from typing import Optional

from pydantic import BaseModel


class Billing(BaseModel):
    class Config:
        orm_mode = True


class BillingBase(Billing):
    date: str
    description: Optional[str]
    amount: Optional[str]
    subscription_interval: Optional[str]
    pay_period: Optional[str]
    subscription_quantity: Optional[str]
    client_name: str
    doctor_name: str
    paid: Optional[bool]
    status: Optional[str]
    date_next_payment_attempt: Optional[str]
