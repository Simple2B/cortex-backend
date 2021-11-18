import datetime
from fastapi import APIRouter, HTTPException, Depends, status
from starlette.responses import FileResponse
from typing import List

from app.services import (
    ClientService,
    QueueService,
    ReportService,
    NoteService,
    VisitService,
)
from app.schemas import (
    ClientInfo,
    Client,
    ClientPhone,
    ClientQueue,
    ClientInTake,
    VisitReportReq,
    VisitReportRes,
    VisitReportResClients,
    Note as NoteSchemas,
    VisitWithNote,
    NoteDelete,
    VisitHistory,
)
from app.models import (
    Client as ClientDB,
    Doctor,
    Reception,
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
    today = datetime.date.today()
    reception = Reception.query.filter(Reception.date == today).first()
    if not reception:
        log(log.INFO, "get_clients: reception didn't created")
        reception = Reception(date=today, doctor_id=doctor.id).save()
        log(log.INFO, "get_clients: Today reception created [%s]", reception)
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
    return service.get_queue(doctor)


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


@router_client.post(
    "/report_visit", response_model=List[VisitReportRes], tags=["Client"]
)
def formed_report_visit(
    client_data: VisitReportReq, doctor: Doctor = Depends(get_current_doctor)
):
    """Filter for page reports visits by date"""
    service = ReportService()
    return service.filter_data_for_report_of_visit(client_data, doctor)


@router_client.get("/report_visit", response_class=FileResponse, tags=["Client"])
async def report_visit(doctor: Doctor = Depends(get_current_doctor)):
    """Get for page reports visits by date"""
    file_report_path = "./visits_report.csv"
    return FileResponse(file_report_path)


@router_client.post(
    "/report_new_clients", response_model=List[VisitReportResClients], tags=["Client"]
)
def formed_report_new_clients(
    client_data: VisitReportReq, doctor: Doctor = Depends(get_current_doctor)
):
    """Filter for page reports new clients by date"""
    service = ReportService()
    return service.filter_data_for_report_of_new_clients(client_data, doctor)


@router_client.get("/report_new_clients", response_class=FileResponse, tags=["Client"])
async def report_new_clients(doctor: Doctor = Depends(get_current_doctor)):
    """Get for page reports visits by date"""
    file_report_path = "./new_clients_report.csv"
    return FileResponse(file_report_path)


@router_client.post("/note", response_model=VisitWithNote, tags=["Client"])
async def write_note(
    data_note: NoteSchemas, doctor: Doctor = Depends(get_current_doctor)
):
    """Write note in visit for client"""
    service = NoteService()
    return service.write_note(data_note, doctor)


@router_client.get("/note/{api_key}", response_model=List[NoteSchemas], tags=["Client"])
async def get_note(api_key: str, doctor: Doctor = Depends(get_current_doctor)):
    """Get notes for client"""
    service = NoteService()
    return service.get_note(api_key, doctor)


@router_client.post("/note_delete", response_model=str, tags=["Client"])
async def delete_note(
    data_note: NoteDelete, doctor: Doctor = Depends(get_current_doctor)
):
    """Delete note"""
    service = NoteService()
    service.delete_note(data_note, doctor)
    return "ok"


@router_client.get(
    "/visit_history/{api_key}", response_model=List[VisitHistory], tags=["Client"]
)
async def get_history_visit(api_key: str, doctor: Doctor = Depends(get_current_doctor)):
    """Get all visits for client"""
    service = VisitService()
    return service.get_history_visit(api_key, doctor)
