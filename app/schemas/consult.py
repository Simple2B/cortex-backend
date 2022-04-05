import datetime
from typing import Optional

from pydantic import BaseModel


class BaseConsult(BaseModel):
    class Config:
        orm_mode = True


class Consult(BaseConsult):
    id: Optional[int]
    date: Optional[datetime.date]
    consult: str
    client_id: int
    doctor_id: int
    visit_id: Optional[int]
    start_time: Optional[str]
    end_time: Optional[str]


class ConsultDelete(BaseConsult):
    id: int
    client_id: int
    doctor_id: int
    visit_id: int
