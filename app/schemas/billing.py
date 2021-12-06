import datetime
from typing import Optional

from pydantic import BaseModel


class Billing(BaseModel):
    class Config:
        orm_mode = True


class BillingBase(Billing):
    date: str
    description: Optional[str]
    amount: Optional[int]
    client_name: str
    doctor_name: str
