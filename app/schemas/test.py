import datetime

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


class GetTest(Test):
    date: str
    client_name: str
    doctor_name: str
