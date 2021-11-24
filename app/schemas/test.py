import datetime

from pydantic import BaseModel


class Test(BaseModel):
    class Config:
        orm_mode = True


class PostTest(Test):
    api_key: str
    date: str


class CreateTest(Test):
    id: int
    date: datetime.datetime
    client_id: int
    doctor_id: int


class GetTest(Test):
    id: int
    date: str
    client_name: str
    doctor_name: str
