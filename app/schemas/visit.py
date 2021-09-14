import datetime
from pydantic import BaseModel


class Visit(BaseModel):
    client_id: int
    doctor_id: int
    data_time: datetime.datetime
    rougue_mode: bool
