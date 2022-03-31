import os
from typing import List

from fastapi import APIRouter, Depends
from starlette.responses import FileResponse

from app.config.settings import Settings

from app.services import ReportService, VisitService

from app.schemas import (
    VisitReportReq,
    VisitReportRes,
    VisitHistory,
    VisitHistoryFilter,
)

from app.models import Doctor

from app.services.auth import get_current_doctor

settings = Settings()
router_client = APIRouter(prefix="/client")


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
