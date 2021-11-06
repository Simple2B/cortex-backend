import datetime
from typing import Optional
from pydantic import BaseModel
from .client import ClientInfo


class Visit(BaseModel):
    date: datetime.date
    start_time: datetime.datetime
    end_time: Optional[datetime.datetime]
    client_id: int
    doctor_id: int
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
    client_info: ClientInfo

    class Config:
        orm_mode = True


class VisitReportResClients(BaseModel):
    client_info: ClientInfo

    class Config:
        orm_mode = True
