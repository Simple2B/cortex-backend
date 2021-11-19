from typing import Optional
from pydantic import BaseModel

from .utils import OrmModeModel


class Doctor(OrmModeModel):
    id: Optional[int]
    first_name: str
    last_name: str
    email: str


class DoctorLogin(BaseModel):
    email: str
    password: str


class DoctorCreate(OrmModeModel):
    api_key: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
