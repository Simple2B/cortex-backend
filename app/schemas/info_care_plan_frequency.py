import datetime

from pydantic import BaseModel


class Info(BaseModel):
    class Config:
        orm_mode = True


class InfoCarePlan(Info):
    care_plan: str


class InfoFrequency(Info):
    frequency: str
