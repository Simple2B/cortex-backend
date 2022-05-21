import datetime
from typing import Optional, List
from pydantic import BaseModel
from .client import ClientInfo


class BaseVisit(BaseModel):
    class Config:
        orm_mode = True


class Visit(BaseVisit):
    date: datetime.date
    start_time: datetime.datetime
    end_time: Optional[datetime.datetime]
    client_id: int
    doctor_id: int
    rougue_mode: bool


class VisitWithNote(BaseVisit):
    id: int
    date: datetime.date
    start_time: datetime.datetime
    end_time: Optional[datetime.datetime]
    client_info: ClientInfo
    notes: Optional[List]


class VisitWithConsult(BaseVisit):
    id: int
    date: datetime.date
    start_time: datetime.datetime
    end_time: Optional[datetime.datetime]
    client_info: ClientInfo
    consult: Optional[List]


class VisitInfoHistory(BaseVisit):
    id: int
    date: datetime.date
    start_time: datetime.datetime
    end_time: Optional[datetime.datetime]
    client_id: int
    doctor_name: Optional[str]
    doctor_id: int
    rougue_mode: bool
    visit_info: VisitWithNote


class VisitHistory(BaseVisit):
    date: str
    doctor_name: str


class VisitHistoryFilter(BaseVisit):
    api_key: str
    start_time: str
    end_time: str


class VisitReportReq(BaseVisit):
    type: str
    start_time: str
    end_time: str


class VisitReportRes(BaseVisit):
    id: Optional[int]
    date: datetime.date
    start_time: datetime.datetime
    end_time: datetime.datetime
    client_info: ClientInfo


class VisitReportResClients(BaseVisit):
    client_info: ClientInfo


class VisitCarePlan(BaseVisit):
    id: Optional[int]
    date: Optional[datetime.date]
    start_time: Optional[datetime.datetime]
    end_time: Optional[datetime.datetime]
    rougue_mode: Optional[bool]
    client_id: Optional[int]
    doctor_id: Optional[int]
