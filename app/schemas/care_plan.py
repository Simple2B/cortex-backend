import datetime
from typing import Optional

from pydantic import BaseModel


class CarePlan(BaseModel):
    class Config:
        orm_mode = True


class CarePlanCreate(CarePlan):
    date: Optional[datetime.datetime]
    start_time: Optional[datetime.datetime]
    end_time: Optional[datetime.datetime]
    progress_date: Optional[str]
    care_plan: Optional[str]
    frequency: Optional[str]
    client_id: int
    doctor_id: int


class InfoCarePlan(CarePlan):
    id: Optional[int]
    date: Optional[datetime.datetime]
    start_time: Optional[str]
    end_time: Optional[str]
    progress_date: Optional[str]
    care_plan: Optional[str]
    frequency: Optional[str]
    client_id: Optional[int]
    doctor_id: Optional[int]


class CarePlanPatientInfo(CarePlan):
    first_visit: Optional[str]
    last_visit: Optional[str]
    total_visits: Optional[str]
    care_plan_length: Optional[str]
    visit_frequency: Optional[str]
    next_visit: Optional[str]
    expiration: Optional[str]


class CarePlanHistory(CarePlan):
    id: Optional[int]
    date: Optional[str]
    start_time: Optional[str]
    end_time: Optional[str]
    care_plan: Optional[str]
    frequency: Optional[str]
    progress_date: Optional[str]
    client_id: Optional[int]
    doctor_id: Optional[int]
    doctor_name: Optional[str]
    notes: Optional[list]
    consults: Optional[list]
    tests: Optional[list]


class CurrentCarePlan(CarePlan):
    id: int
    date: Optional[str]
    start_time: Optional[str]
    end_time: Optional[str]
    care_plan: Optional[str]
    frequency: Optional[str]
    progress_date: Optional[str]
    client_id: int
    doctor_id: int
