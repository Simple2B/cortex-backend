import datetime
from typing import Optional
from pydantic import BaseModel

from .client import ClientInfo
from .utils import OrmModeModel


class Visit(OrmModeModel):
    date: datetime.date
    start_time: datetime.datetime
    end_time: Optional[datetime.datetime]
    client_id: int
    doctor_id: int
    rougue_mode: bool


class VisitWithNote(OrmModeModel):
    id: int
    date: datetime.date
    start_time: datetime.datetime
    end_time: Optional[datetime.datetime]
    client_info: ClientInfo
    notes: Optional[list]


class VisitInfoHistory(OrmModeModel):
    id: int
    date: datetime.date
    start_time: datetime.datetime
    end_time: Optional[datetime.datetime]
    client_id: int
    doctor_name: str
    doctor_id: int
    rougue_mode: bool
    visit_info: VisitWithNote


class VisitHistory(OrmModeModel):
    date: str
    doctor_name: str


class VisitReportReq(OrmModeModel):
    type: str
    start_time: str
    end_time: str


class VisitReportRes(OrmModeModel):
    id: Optional[int]
    date: datetime.date
    start_time: datetime.datetime
    end_time: datetime.datetime
    client_info: ClientInfo


class VisitReportResClients(OrmModeModel):
    client_info: ClientInfo
