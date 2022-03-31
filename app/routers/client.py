import datetime
from typing import List

# import stripe

from fastapi import APIRouter, HTTPException, Depends, status
from fastapi_pagination import Page as BasePage

# from stripe.api_resources import line_item, payment_method
from app.config.settings import Settings

from app.services import (
    ClientService,
    QueueService,
)
from app.schemas import (
    ClientInfo,
    Client,
    ClientPhone,
)
from app.models import (
    Client as ClientDB,
    Doctor,
    Reception,
)
from app.services.auth import get_current_doctor
from app.logger import log


# from app.config import settings as config

settings = Settings()
router_client = APIRouter(prefix="/client")
Page = BasePage.with_custom_options(size=4)
PageClients = BasePage.with_custom_options(size=6)


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
    return {
        "id": client.id,
        "api_key": client.api_key,
        "first_name": client.first_name,
        "last_name": client.last_name,
        "phone": client.phone,
        "email": client.email,
        "req_date": client.req_date.strftime("%m/%d/%Y, %H:%M:%S")
        if client.req_date
        else None,
    }


@router_client.get("/kiosk/{phone}", response_model=Client, tags=["Client"])
async def get_client_with_phone(
    phone: str, doctor: Doctor = Depends(get_current_doctor)
):
    """Get client with phone"""
    client = QueueService.get_client_with_phone(phone)
    if not client:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Client not found"
        )
    return {
        "id": client.id,
        "api_key": client.api_key,
        "first_name": client.first_name,
        "last_name": client.last_name,
        "phone": client.phone,
        "email": client.email,
        "req_date": client.req_date.strftime("%m/%d/%Y, %H:%M:%S")
        if client.req_date
        else None,
    }


@router_client.get("/clients", response_model=List[Client], tags=["Client"])
def get_clients(doctor: Doctor = Depends(get_current_doctor)):
    """Show clients"""
    today = datetime.date.today()
    reception = Reception.query.filter(Reception.date == today).first()
    if not reception:
        log(log.INFO, "get_clients: reception didn't created")
        reception = Reception(date=today, doctor_id=doctor.id).save()
        log(log.INFO, "get_clients: Today reception created [%s]", reception)
    clients_from_db = ClientDB.query.all()
    clients = [
        {
            "id": client.id,
            "api_key": client.api_key,
            "first_name": client.first_name,
            "last_name": client.last_name,
            "phone": client.phone,
            "email": client.email,
            "req_date": client.req_date.strftime("%m/%d/%Y, %H:%M:%S")
            if client.req_date
            else None,
            "visits": client.client_info["visits"]
            if client.client_info["visits"]
            else [],
        }
        for client in clients_from_db
    ]
    return clients
