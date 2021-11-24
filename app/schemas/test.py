import datetime
from typing import Optional

from pydantic import BaseModel


class Test(BaseModel):
    class Config:
        orm_mode = True


class PostTest(Test):
    api_key: str
    date: str


class CreateTest(Test):
    id: int
    date: Optional[datetime.datetime]
    client_id: int
    doctor_id: int
    care_plan: Optional[str]
    frequency: Optional[str]


class GetTest(Test):
    id: int
    date: str
    client_name: str
    doctor_name: str


class PostTestCarePlanAndFrequency(Test):
    test_id: int
    api_key: str
    care_plan: str
    frequency: str
