from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from app.services import AuthService, get_current_doctor
from app.schemas import DoctorCreate, Doctor, Token
from app.models import Reception


router = APIRouter(prefix="/auth")


@router.post("/sign_up", response_model=Doctor, tags=["Auth"])
async def sign_up(doctor_data: DoctorCreate):
    """Register new user"""
    service = AuthService()
    doctor = service.register_new_doctor(doctor_data)
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor with this key not found")
    return doctor


@router.post("/sign_in", response_model=Token, tags=["Auth"])
async def sign_in(form_data: OAuth2PasswordRequestForm = Depends()):
    """Login"""
    service = AuthService()
    return service.authenticate_doctor(form_data.username, form_data.password)


@router.get("/doctor", response_model=Doctor, tags=["Auth"])
def get_user(doctor: Doctor = Depends(get_current_doctor)):
    """Show current authenticated doctor"""
    Reception(doctor_id=doctor.id).save()
    return doctor
