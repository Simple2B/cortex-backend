from fastapi import APIRouter, HTTPException
from typing import List

# from fastapi.security import OAuth2PasswordBearer

from app.services import ClientService, QueueService
from app.schemas import ClientInfo, Client, Queue
from app.models import Client as ClientDB, QueueMember as QueueMemberDB


router_client = APIRouter(prefix="/client")


@router_client.post("/registration", response_model=Client, tags=["Client"])
async def registrations(client_data: ClientInfo):
    """Register new client"""
    service = ClientService()
    client = service.register_new_client(client_data)
    if not client:
        raise HTTPException(status_code=404, detail="Client didn't registration")
    return client


@router_client.get("/clients", response_model=List[Client], tags=["Client"])
def get_clients():
    """Show clients"""
    return ClientDB.query.all()


@router_client.post("/add_clients_queue", response_model=str, tags=["Client"])
async def add_client_to_queue(client_data: ClientInfo):
    """Put clients to queue"""
    service = QueueService()
    service.add_client_to_queue(client_data)
    # if not client:
    #     raise HTTPException(status_code=404, detail="Client didn't add to queue")
    return "ok"


@router_client.get("/queue", response_model=List[Queue], tags=["Client"])
def get_queue():
    """Show queue"""
    return QueueMemberDB.query.all()
