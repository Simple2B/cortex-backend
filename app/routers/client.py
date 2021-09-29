from fastapi import APIRouter, Depends, HTTPException

from app.services import AuthService, get_current_doctor
from app.schemas import ClientCreate, Client


routerClient = APIRouter(prefix="/client")


@routerClient.post("/registration", response_model=Client, tags=["Client"])
async def registrations(client_data: ClientCreate):
    """Register new client"""
    service = AuthService()
    client = service.register_new_client(client_data)
    if not client:
        raise HTTPException(status_code=404, detail="Client didn't registration")
    return client
