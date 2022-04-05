import datetime
from typing import Optional

from pydantic import BaseModel


class BaseNote(BaseModel):
    class Config:
        orm_mode = True


class Note(BaseNote):
    id: Optional[int]
    date: Optional[datetime.date]
    notes: str
    client_id: int
    doctor_id: int
    visit_id: Optional[int]
    start_time: Optional[str]
    end_time: Optional[str]


class NoteDelete(BaseNote):
    id: int
    client_id: int
    doctor_id: int
    visit_id: int
