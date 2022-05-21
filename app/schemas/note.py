import datetime
from typing import Optional

from pydantic import BaseModel

# from stripe import api_key


class BaseNote(BaseModel):
    class Config:
        orm_mode = True


class Note(BaseNote):
    id: Optional[int]
    date: Optional[datetime.date]
    notes: str
    api_key: Optional[str]
    doctor_id: int
    visit_id: Optional[int]
    start_time: Optional[str]
    end_time: Optional[str]


class NoteDelete(BaseNote):
    id: int
    api_key: str
    doctor_id: int
    visit_id: int
