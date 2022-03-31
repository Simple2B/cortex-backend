from typing import List

from fastapi import APIRouter, Depends

from app.services import NoteService

from app.schemas import (
    Note as NoteSchemas,
    VisitWithNote,
    NoteDelete,
)

from app.models import Doctor
from app.services.auth import get_current_doctor

router_client = APIRouter(prefix="/client")


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
