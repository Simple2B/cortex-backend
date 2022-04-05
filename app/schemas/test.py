import datetime
from typing import Optional

from pydantic import BaseModel


class Test(BaseModel):
    class Config:
        orm_mode = True


class PostTest(Test):
    api_key: str
    date: str
    start_time: Optional[str]
    end_time: Optional[str]
    current_care_plan_id: int


class DeleteTest(Test):
    id: int
    api_key: str
    current_care_plan_id: int


class CreateTest(Test):
    id: int
    date: Optional[datetime.datetime]
    care_plan_id: int
    client_id: int
    doctor_id: int


class GetTest(Test):
    id: int
    date: str
    client_name: str
    doctor_name: str
    care_plan_id: Optional[int]
    care_plan: Optional[str]
    frequency: Optional[str]


class PostTestCarePlanAndFrequency(Test):
    test_id: int
    api_key: str
    progress_date: Optional[str]
    care_plan: str
    frequency: str
