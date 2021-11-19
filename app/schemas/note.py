import datetime
from typing import Optional
from pydantic import BaseModel


class Note(BaseModel):
    id: Optional[int]
    date: Optional[datetime.date]
    notes: str
    client_id: int
    doctor_id: int
    visit_id: int

    class Config:
        orm_mode = True


class NoteDelete(BaseModel):
    id: int
    client_id: int
    doctor_id: int
    visit_id: int

    class Config:
        orm_mode = True
