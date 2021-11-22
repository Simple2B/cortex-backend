from typing import List
from fastapi import APIRouter, Depends

from app.models import Doctor
from app.schemas import PostTest, CreateTest, GetTest
from app.services import TestService
from app.services.auth import get_current_doctor


router_test = APIRouter(prefix="/test")


@router_test.post("/test_create", response_model=CreateTest, tags=["Test"])
async def sign_up(data: PostTest, doctor: Doctor = Depends(get_current_doctor)):
    """Create test for client in visit"""
    service = TestService()
    return service.create_test(data, doctor)


@router_test.get(
    "/client_tests/{api_key}", response_model=List[GetTest], tags=["Client"]
)
async def get_client_tests(api_key: str, doctor: Doctor = Depends(get_current_doctor)):
    """Get all tests for client"""
    service = TestService()
    return service.get_client_tests(api_key, doctor)
