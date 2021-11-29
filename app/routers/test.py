from typing import List
from fastapi import APIRouter, Depends

from app.models import Doctor
from app.schemas import (
    PostTest,
    CreateTest,
    GetTest,
    PostTestCarePlanAndFrequency,
    InfoCarePlan,
    CarePlanCreate,
    ClientCarePlan,
)
from app.services import TestService
from app.services.auth import get_current_doctor


router_test = APIRouter(prefix="/test")


@router_test.post("/care_plan_create", response_model=CarePlanCreate, tags=["Test"])
async def care_plan_create(
    data: ClientCarePlan, doctor: Doctor = Depends(get_current_doctor)
):
    """Create care_plan for client"""
    service = TestService()
    return service.care_plan_create(data, doctor)


@router_test.post("/test_create", response_model=CreateTest, tags=["Test"])
async def test_create(data: PostTest, doctor: Doctor = Depends(get_current_doctor)):
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


@router_test.post("/care_plan_frequency", response_model=CreateTest, tags=["Test"])
async def write_care_plan_frequency(
    data: PostTestCarePlanAndFrequency, doctor: Doctor = Depends(get_current_doctor)
):
    """Add to test care plan and frequency"""
    service = TestService()
    return service.write_care_plan_frequency(data, doctor)


@router_test.get("/care_plan_names", response_model=List[InfoCarePlan], tags=["Client"])
async def get_care_plan_names(doctor: Doctor = Depends(get_current_doctor)):
    """Get all care plan name"""
    service = TestService()
    return service.get_care_plan_names(doctor)


@router_test.get("/test/{test_id}", response_model=GetTest, tags=["Client"])
async def get_test(test_id: str, doctor: Doctor = Depends(get_current_doctor)):
    """Get test with id"""
    service = TestService()
    return service.get_test(test_id, doctor)
