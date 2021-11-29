import datetime
from typing import Optional

from pydantic import BaseModel


class CarePlan(BaseModel):
    class Config:
        orm_mode = True


class CarePlanCreate(CarePlan):
    date: Optional[datetime.datetime]
    care_plan: Optional[str]
    frequency: Optional[str]
    client_id: int
    doctor_id: int
