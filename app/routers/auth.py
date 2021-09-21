from fastapi import APIRouter, Depends


from app.services import AuthService, get_current_doctor
from app.schemas import DoctorCreate, Doctor, Token


router = APIRouter(prefix="/auth")


@router.post("/sign_up", response_model=Doctor, tags=["Auth"])
async def sign_up(doctor_data: DoctorCreate):
    """Register new user"""
    # TODO only admin could create user
    service = AuthService()
    return await service.register_new_doctor(doctor_data)


@router.post("/sign_in", response_model=Token, tags=["Auth"])
async def sign_in(form_data: DoctorCreate):
    """Login"""
    service = AuthService()
    return await service.authenticate_doctor(form_data.email, form_data.password)


@router.get("/doctor", response_model=Doctor, tags=["Auth"])
def get_user(doctor: Doctor = Depends(get_current_doctor)):
    """Show current authenticated doctor"""
    return doctor
