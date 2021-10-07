from fastapi import APIRouter, HTTPException, Depends
from typing import List

# from fastapi.security import OAuth2PasswordBearer

from app.services import ClientService, QueueService
from app.schemas import ClientInfo, Client
from app.models import Client as ClientDB, QueueMember as QueueMemberDB, Doctor
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


# @router_client.post("/create_reception", response_model=str, tags=["Client"])
# def create_reception(doctor: Doctor = Depends(get_current_doctor):
#     """Create reception for clients"""
#         reception = Reception(date=datetime.datetime.now(), doctor_id=doctor.id)
#         reception.save()

#         return "ok"


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
    # if not client:
    #     raise HTTPException(status_code=404, detail="Client didn't add to queue")
    return "ok"


@router_client.get("/queue", response_model=List[Client], tags=["Client"])
def get_queue(doctor: Doctor = Depends(get_current_doctor)):
    """Show queue"""
    queue = []
    queue_members = QueueMemberDB.query.all()
    clients = ClientDB.query.all()
    for queue_member in queue_members:
        for client in clients:
            if queue_member.id == client.id:
                queue.append(client)
    return queue
