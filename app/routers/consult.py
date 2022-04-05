from typing import List

# import stripe

from fastapi import APIRouter, Depends

from app.config.settings import Settings
from app.schemas.consult import ConsultDelete

from app.services import (
    ConsultService,
)
from app.schemas import (
    Consult as ConsultSchemas,
)
from app.models import Doctor
from app.services.auth import get_current_doctor

# from app.config import settings as config

settings = Settings()
router_consult = APIRouter(prefix="/consult")


@router_consult.post("/write_consult", response_model=ConsultSchemas, tags=["Consult"])
async def write_consult(
    data_consult: ConsultSchemas, doctor: Doctor = Depends(get_current_doctor)
):
    """Write consult in visit for client"""
    service = ConsultService()
    return service.write_consult(data_consult, doctor)


@router_consult.get(
    "/get_consult/{api_key}", response_model=List[ConsultSchemas], tags=["Consult"]
)
async def get_consult(api_key: str, doctor: Doctor = Depends(get_current_doctor)):
    """Get notes for client"""
    service = ConsultService()
    return service.get_consult(api_key, doctor)


@router_consult.post("/consult_delete", response_model=str, tags=["Consult"])
async def delete_consult(
    data_consult: ConsultDelete, doctor: Doctor = Depends(get_current_doctor)
):
    """Delete note"""
    service = ConsultService()
    service.delete_consult(data_consult, doctor)
    return "ok"
