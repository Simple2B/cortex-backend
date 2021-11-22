from fastapi import APIRouter, Depends

from app.models import Doctor
from app.schemas import PostTest, CreateTest
from app.services import TestService
from app.services.auth import get_current_doctor


router_test = APIRouter(prefix="/test")


@router_test.post("/test", response_model=CreateTest, tags=["Test"])
async def sign_up(data: PostTest, doctor: Doctor = Depends(get_current_doctor)):
    """Create test for client in visit"""
    service = TestService()
    return service.create_test(data, doctor)
