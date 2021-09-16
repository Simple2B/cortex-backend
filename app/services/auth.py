from datetime import datetime, timedelta

from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.hash import bcrypt
from pydantic import ValidationError

from app.schemas import Doctor, Token, DoctorCreate
from app.models import Doctor as DoctorDB
from app.config import settings as config
from app.logger import log


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/sign_in")


def get_current_doctor(token: str = Depends(oauth2_scheme)) -> Doctor:
    return AuthService.validate_token(token)


class AuthService:
    def register_new_doctor(self, doctor_data: DoctorCreate) -> Doctor:
        doctor = DoctorDB(
            # first_name=doctor_data.first_name,
            # last_name=doctor_data.last_name,
            email=doctor_data.email,
            hash_password=self.hash_password(doctor_data.password),
        )
        log(log.INFO, "Doctor %s has been created", doctor_data.first_name)
        return doctor

    def authenticate_doctor(self, email: str, password: str) -> Token:
        def exception():
            return HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )

        doctor = DoctorDB.query.filter(email=email).first()

        if not doctor:
            log(log.ERROR, "Doctor %s does not exist", email)
            raise exception()

        if not self.verify_password(password, doctor.hash_password):
            log(log.ERROR, "Password is not correct")
            raise exception()

        log(log.INFO, "Doctor has been logged")
        return self.create_token(doctor)

    @classmethod
    def verify_password(cls, password: str, hashed_password: str) -> bool:
        return bcrypt.verify(password, hashed_password)

    @classmethod
    def hash_password(cls, password: str) -> str:
        return bcrypt.hash(password)

    @classmethod
    def validate_token(cls, token: str) -> Doctor:
        exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

        try:
            payload = jwt.decode(
                token, config.JWT_SECRET, algorithms=[config.JWT_ALGORITHM]
            )
        except JWTError:
            log(log.ERROR, "JWT token could not create")
            raise exception from None

        doctor_data = payload.get("doctor")

        try:
            doctor = Doctor.parse_obj(doctor_data)
        except ValidationError:
            raise exception from None

        return doctor

    @classmethod
    def create_token(cls, doctor: DoctorDB) -> Token:
        doctor_data = Doctor.from_orm(doctor)

        now = datetime.utcnow()
        payload = {
            "iat": now,
            "nbf": now,
            "exp": now + timedelta(seconds=int(config.JWT_EXP)),
            "sub": str(doctor_data.id),
            "doctor": doctor_data.dict(),
        }
        token = jwt.encode(payload, config.JWT_SECRET, algorithm=config.JWT_ALGORITHM)
        return Token(access_token=token)
