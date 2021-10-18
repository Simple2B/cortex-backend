from datetime import datetime, timedelta

from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from pydantic import ValidationError
from sqlalchemy import func

from app.schemas import Doctor, Token, DoctorCreate
from app.models import Doctor as DoctorDB
from app.config import settings as config
from app.logger import log


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/sign_in")


def get_current_doctor(token: str = Depends(oauth2_scheme)) -> Doctor:
    return AuthService.validate_token(token)


class AuthService:
    def register_new_doctor(self, doctor_data: DoctorCreate) -> Doctor:
        doctor = DoctorDB.query.filter(
            func.lower(DoctorDB.api_key) == func.lower(doctor_data.api_key)
        ).first()
        if doctor:
            doctor.email_approved = True
            doctor.password = doctor_data.password
            doctor.save()
            log(log.INFO, "Doctor [%s] has been approved", doctor.first_name)
            return Doctor.from_orm(doctor)
        return None

    def authenticate_doctor(self, username: str, password: str) -> Token:
        doctor = DoctorDB.authenticate(email=username, password=password)
        if not doctor:
            log(log.ERROR, "Authentication failed")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )

        log(log.INFO, "Doctor has been logged")
        return self.create_token(doctor)

    @classmethod
    def validate_token(cls, token: str) -> Doctor:
        try:
            payload = jwt.decode(
                token, config.JWT_SECRET, algorithms=[config.JWT_ALGORITHM]
            )
        except JWTError:
            log(log.ERROR, "Invalid JWT token")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid JWT token",
                headers={"WWW-Authenticate": "Bearer"},
            )

        doctor_data = payload.get("doctor")

        try:
            return Doctor.parse_obj(doctor_data)
        except ValidationError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate doctor data",
                headers={"WWW-Authenticate": "Bearer"},
            )

    @classmethod
    def create_token(cls, doctor: DoctorDB) -> Token:
        doctor_data = Doctor.from_orm(doctor)

        now = datetime.utcnow()
        payload = {
            "iat": now,
            "nbf": now,
            "exp": now + timedelta(seconds=int(config.JWT_EXP)),
            "sub": str(doctor.id),
            "doctor": doctor_data.dict(),
        }
        token = jwt.encode(payload, config.JWT_SECRET, algorithm=config.JWT_ALGORITHM)
        return Token(access_token=token)
