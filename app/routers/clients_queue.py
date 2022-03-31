from typing import List

from fastapi import APIRouter, Depends

from app.services import ClientService, QueueService
from app.schemas import Client, ClientQueue, ClientInTake

from app.models import Doctor

from app.services.auth import get_current_doctor
from app.logger import log

router_client = APIRouter(prefix="/client")


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
    return service.get_queue(doctor)
