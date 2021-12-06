import datetime
from typing import Optional

from pydantic import BaseModel


class Billing(BaseModel):
    class Config:
        orm_mode = True


class BillingBase(Billing):
    description: Optional[str]
    amount: int
    client_id: int
    doctor_id: int
