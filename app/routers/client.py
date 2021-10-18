import datetime

# from sqlalchemy import and_
from fastapi import APIRouter, HTTPException, Depends
from typing import List

from app.services import ClientService, QueueService
from app.schemas import ClientInfo, Client, ClientPhone
from app.models import (
    Client as ClientDB,
    QueueMember as QueueMemberDB,
    Doctor,
    Reception,
    ClientCondition,
    Condition,
    ClientDisease,
    Disease,
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
        raise HTTPException(status_code=404, detail="Client didn't registration")
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
    # reception = Reception.query.filter(
    #     and_(
    #         Reception.doctor_id == doctor.id,
    #         Reception.date == date,
    #     )
    # ).first()
    reception = Reception.query.filter(Reception.date == date).first()
    if reception:
        return reception.queue_members
    return


@router_client.get("/client_intake", response_model=ClientInfo, tags=["Client"])
async def client_intake(api_key: str, doctor: Doctor = Depends(get_current_doctor)):
    """Show client for Intake"""
    data_clients = ClientDB.query.all()
    client_intake: ClientInfo = {}

    for client in data_clients:
        if client.api_key == api_key:
            log(log.INFO, "Client [%s] for intake", client)
            link_condition = ClientCondition.query.filter(
                ClientCondition.client_id == client.id
            ).first()
            conditions = Condition.query.filter(
                Condition.id == link_condition.condition_id
            ).all()

            link_diseases = ClientDisease.query.filter(
                ClientDisease.client_id == client.id
            ).first()
            diseases = Disease.query.filter(
                Disease.id == link_diseases.disease_id
            ).all()

            client_intake = {
                "id": client.id,
                "firstName": client.first_name,
                "lastName": client.last_name,
                "birthday": client.birthday.strftime("%m/%d/%Y"),
                "address": client.address,
                "city": client.city,
                "state": client.state,
                "zip": client.zip,
                "phone": client.phone,
                "email": client.email,
                "referring": client.referring,
                "conditions": conditions,
                "otherCondition": "",
                "diseases": diseases,
                "medications": client.medications,
                "covidTestedPositive": client.covid_tested_positive,
                "covidVaccine": client.covid_vaccine,
                "stressfulLevel": client.stressful_level,
                "consentMinorChild": client.consent_minor_child,
                "relationshipChild": client.relationship_child,
            }
            client_in_queue = QueueMemberDB.query.filter(
                QueueMemberDB.client_id == client.id
            ).first()
            if client_in_queue:
                # client_in_queue.delete()
                log(log.INFO, "Client in queue [%s] deleted", client_in_queue)
            return client_intake
