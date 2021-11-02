import datetime
from typing import Optional
from pydantic import BaseModel
from .client import ClientInfo


class Visit(BaseModel):
    client_id: int
    doctor_id: int
    date: datetime.date
    start_time: datetime.datetime
    rougue_mode: bool

    class Config:
        orm_mode = True


class VisitReportReq(BaseModel):
    type: str
    start_time: str
    end_time: str

    class Config:
        orm_mode = True


class VisitReportRes(BaseModel):
    id: Optional[int]
    date: datetime.date
    start_time: datetime.datetime
    end_time: datetime.datetime
    # client: str
    client_info: ClientInfo
    # doctor: str

    class Config:
        orm_mode = True
