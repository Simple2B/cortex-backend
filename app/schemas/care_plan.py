import datetime
from typing import Optional

from pydantic import BaseModel


class CarePlan(BaseModel):
    class Config:
        orm_mode = True


class CarePlanCreate(CarePlan):
    date: Optional[datetime.datetime]
    progress_date: Optional[str]
    care_plan: Optional[str]
    frequency: Optional[str]
    client_id: int
    doctor_id: int


class CarePlanPatientInfo(CarePlan):
    first_visit: Optional[str]
    last_visit: Optional[str]
    total_visits: Optional[str]
    care_plan_length: Optional[str]
    visit_frequency: Optional[str]
    next_visit: Optional[str]
    expiration: Optional[str]
