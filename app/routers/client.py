from fastapi import APIRouter, HTTPException, Depends, status
from typing import List
from app.schemas.client import ClientInTake

from app.services import ClientService, QueueService, ReportService
from app.schemas import (
    ClientInfo,
    Client,
    ClientPhone,
    ClientQueue,
    VisitReportReq,
    VisitReportRes,
)
from app.models import (
    Client as ClientDB,
    Doctor,
)
from app.services.auth import get_current_doctor
from app.logger import log

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


@router_client.get("/kiosk/{phone}", response_model=Client, tags=["Client"])
async def get_client_with_phone(
    phone: str, doctor: Doctor = Depends(get_current_doctor)
):
    """Get client with phone"""
    return QueueService.get_client_with_phone(phone)


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


@router_client.post("/complete_client_visit", response_model=str, tags=["Client"])
async def complete_client_visit(
    client_data: ClientInTake, doctor: Doctor = Depends(get_current_doctor)
):
    """Put clients to queue"""
    log(log.INFO, "client to queue: Client data [%s]", client_data)
    service = ClientService()
    service.complete_client_visit(client_data, doctor)
    return "ok"


@router_client.post("/delete_clients_queue", response_model=str, tags=["Client"])
async def delete_client_from_queue(
    client_data: ClientQueue, doctor: Doctor = Depends(get_current_doctor)
):
    """Delete client from queue"""
    service = QueueService()
    service.delete_client_from_queue(client_data, doctor)
    return "ok"


@router_client.get("/queue", response_model=List[ClientQueue], tags=["Client"])
def get_queue(doctor: Doctor = Depends(get_current_doctor)):
    """Show clients in queue"""
    service = QueueService()
    queue_members = service.get_queue(doctor)
    return queue_members


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


# filtering for reports page
@router_client.post("/report", response_model=List[VisitReportRes], tags=["Client"])
def formed_report(
    client_data: VisitReportReq, doctor: Doctor = Depends(get_current_doctor)
):
    """Filter for page reports by date"""
    service = ReportService()
    reports = service.filter_data_for_report(client_data, doctor)
    return reports
