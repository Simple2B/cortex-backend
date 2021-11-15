import datetime
from typing import Optional
from pydantic import BaseModel


class Note(BaseModel):
    date: datetime.date
    notes: str
    client_id: int
    doctor_id: int

    class Config:
        orm_mode = True