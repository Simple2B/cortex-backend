import datetime

from pydantic import BaseModel


class BaseResponsePydantic(BaseModel):
    date: datetime.datetime
    doctor_id: int
