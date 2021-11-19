import datetime
from typing import Optional
from pydantic import BaseModel

from .utils import OrmModeModel


class Note(OrmModeModel):
    id: Optional[int]
    date: Optional[datetime.date]
    notes: str
    client_id: int
    doctor_id: int
    visit_id: int


class NoteDelete(OrmModeModel):
    id: int
    client_id: int
    doctor_id: int
    visit_id: int
