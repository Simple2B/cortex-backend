import datetime

from sqlalchemy import and_
from fastapi import APIRouter, HTTPException, Depends, status
from typing import List
from app.schemas.client import ClientInTake

from app.services import ClientService, QueueService
from app.schemas import ClientInfo, Client, ClientPhone
from app.models import (
    Client as ClientDB,
    QueueMember as QueueMemberDB,
    Doctor,
    Reception,
)
from app.services.auth import get_current_doctor


router_client = APIRouter(prefix="/client")


@router_client.post("/registration", response_model=Client, tags=["Client"])
async def registrations(client_data: ClientInfo):
    """Register new client"""
    service = ClientService()
    client = service.register_new_client(client_data)
    if not client:
        raise HTTPException(status_code=404, detail="Client didn't registration")
    return client


@router_client.post("/kiosk", response_model=Client, tags=["Client"])
async def identify_client_with_phone(
    phone_data: ClientPhone, doctor: Doctor = Depends(get_current_doctor)
):
    """Identify client with phone"""
    service = QueueService()
    client = service.identify_client_with_phone(phone_data, doctor)
    if not client:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Client not found"
        )
    return client


@router_client.get("/clients", response_model=List[Client], tags=["Client"])
def get_clients(doctor: Doctor = Depends(get_current_doctor)):
    """Show clients"""
    return ClientDB.query.all()


@router_client.post("/add_clients_queue", response_model=str, tags=["Client"])
async def add_client_to_queue(
    client_data: Client, doctor: Doctor = Depends(get_current_doctor)
):
    """Put clients to queue"""
    service = QueueService()
    service.add_client_to_queue(client_data, doctor)
    return "ok"


@router_client.get("/queue", response_model=List[Client], tags=["Client"])
def get_queue(doctor: Doctor = Depends(get_current_doctor)):
    """Show queue"""
    date = datetime.date.today()
    reception = Reception.query.filter(Reception.date == date).first()
    queue_members = QueueMemberDB.query.filter(
        and_(
            QueueMemberDB.reception_id == reception.id,
            QueueMemberDB.visit_id == None,  # noqa E711
            QueueMemberDB.canceled == False,
        )
    ).all()
    return [member.client for member in queue_members]


@router_client.post("/client_intake", response_model=ClientInfo, tags=["Client"])
async def client_intake(
    client_data: ClientInTake, doctor: Doctor = Depends(get_current_doctor)
):
    """Put client intake and returns it"""
    return ClientService.intake(client_data, doctor)


@router_client.get("/client_intake", response_model=ClientInfo, tags=["Client"])
async def get_client_intake(doctor: Doctor = Depends(get_current_doctor)):
    """Put client intake and returns it"""
    return ClientService.get_intake(doctor)
