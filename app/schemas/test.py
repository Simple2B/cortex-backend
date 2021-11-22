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
    date: datetime.datetime
    client_id: int
    doctor_id: int
