import os
import datetime
from typing import List

# import stripe

from fastapi import APIRouter, HTTPException, Depends, status, Request, Header
from fastapi_pagination import Page as BasePage, paginate
from starlette.responses import FileResponse

# from stripe.api_resources import line_item, payment_method
from app.config.settings import Settings

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
    Note as NoteSchemas,
    VisitWithNote,
    NoteDelete,
    VisitHistory,
    VisitHistoryFilter,
    DoctorStripeSecret,
    ClientInfoStripe,
    BillingBase,
    ClientStripeSubscription,
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
    return client


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


@router_client.get(
    "/clients_for_queue", response_model=PageClients[Client], tags=["Client"]
)
async def get_db_clients_for_queue(
    # query: Optional[str],
    doctor: Doctor = Depends(get_current_doctor),
):
    """Show clients from db for queue"""
    today = datetime.date.today()
    reception = Reception.query.filter(Reception.date == today).first()
    if not reception:
        log(log.INFO, "get_db_clients_for_queue: reception didn't created")
        reception = Reception(date=today, doctor_id=doctor.id).save()
        log(
            log.INFO,
            "get_db_clients_for_queue: Today reception created [%s]",
            reception,
        )
    clients = ClientDB.query.all()

    log(log.INFO, "get_db_clients_for_queue: clients count [%d]", len(clients))

    return paginate(clients)



























###############################################################################################################
# intake
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






################################################################################################################
# queue
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








###############################################################################################################
# visits
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
    return FileResponse(os.path.join(settings.REPORTS_DIR, settings.VISITS_REPORT_FILE))


@router_client.post("/report_new_clients", response_model=str, tags=["Client"])
def formed_report_new_clients(
    client_data: VisitReportReq, doctor: Doctor = Depends(get_current_doctor)
):
    """Filter for page reports new clients by date"""
    service = ReportService()
    service.filter_data_for_report_of_new_clients(client_data, doctor)
    return "ok"


@router_client.get("/report_new_clients", response_class=FileResponse, tags=["Client"])
async def report_new_clients(doctor: Doctor = Depends(get_current_doctor)):
    """Get for page reports visits by date"""
    return FileResponse(
        os.path.join(settings.REPORTS_DIR, settings.CLIENTS_REPORT_FILE)
    )


@router_client.get(
    "/visit_history/{api_key}", response_model=List[VisitHistory], tags=["Client"]
)
async def get_history_visit(api_key: str, doctor: Doctor = Depends(get_current_doctor)):
    """Get all visits for client"""
    service = VisitService()
    return service.get_history_visit(api_key, doctor)


@router_client.post(
    "/visit_history", response_model=List[VisitHistory], tags=["Client"]
)
async def filter_visits(
    data: VisitHistoryFilter, doctor: Doctor = Depends(get_current_doctor)
):
    """Filtered history visits"""
    service = VisitService()
    return service.filter_visits(data, doctor)







##################################################################################################################
# note
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







####################################################################################################################
# stripe
# @router_client.get("/get_secret", response_model=DoctorStripeSecret, tags=["Client"])
# async def get_secret(doctor: Doctor = Depends(get_current_doctor)):
#     """Get secret stripe keys"""
#     service = VisitService()

#     return service.get_secret()


# @router_client.post("/create_stripe_session", response_model=str, tags=["Client"])
# async def create_stripe_session(
#     data: ClientInfoStripe, doctor: Doctor = Depends(get_current_doctor)
# ):
#     """Stripe session"""
#     service = VisitService()
#     return service.create_stripe_session(data, doctor)


# @router_client.post("/create_stripe_subscription", response_model=str, tags=["Client"])
# async def stripe_subscription(
#     data: ClientStripeSubscription, doctor: Doctor = Depends(get_current_doctor)
# ):
#     """Stripe session"""
#     service = VisitService()
#     return service.stripe_subscription(data, doctor)


# @router_client.post("/webhook", response_model=str, tags=["Client"])
# async def webhook(request: Request, stripe_signature: str = Header(None)):
#     """Stripe webhook"""
#     service = VisitService()
#     service.webhook(request, stripe_signature)
#     return "ok"


# @router_client.get(
#     "/billing_history/{api_key}", response_model=Page[BillingBase], tags=["Client"]
# )
# async def get_billing_history(
#     api_key: str, doctor: Doctor = Depends(get_current_doctor)
# ):
#     """Get secret stripe keys"""
#     service = VisitService()
#     billing_history = service.get_billing_history(api_key, doctor)

#     return paginate(billing_history)
