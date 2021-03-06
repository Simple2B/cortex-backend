from typing import Optional
from pydantic import BaseModel, EmailStr


class Doctor(BaseModel):
    id: Optional[int]
    first_name: str
    last_name: str
    email: Optional[EmailStr]

    class Config:
        orm_mode = True


class DoctorLogin(BaseModel):
    email: str
    password: str


class DoctorCreate(BaseModel):
    api_key: str
    password: str

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class DoctorStripeSecret(BaseModel):
    pk_test: str
    sk_test: str
    cortex_key: str

    class Config:
        orm_mode = True
