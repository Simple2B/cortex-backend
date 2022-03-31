from fastapi import APIRouter, Depends

from app.services import ClientService

from app.schemas import ClientInfo, ClientInTake

from app.models import Doctor

from app.services.auth import get_current_doctor

router_client = APIRouter(prefix="/client")


@router_client.post("/client_intake", response_model=ClientInfo, tags=["Client"])
async def client_intake(
    client_data: ClientInTake, doctor: Doctor = Depends(get_current_doctor)
):
    """Put client intake and returns it"""
    return ClientService.intake(client_data, doctor)


@router_client.get(
    "/client_intake/{api_key}", response_model=ClientInfo, tags=["Client"]
)
async def get_client_intake(api_key: str, doctor: Doctor = Depends(get_current_doctor)):
    """Returns client intake"""
    return ClientService.get_intake(api_key, doctor)