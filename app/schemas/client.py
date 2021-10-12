from pydantic import BaseModel, EmailStr
from typing import Optional


class ClientInfo(BaseModel):
    firstName: str
    lastName: str
    birthday: Optional[str]
    address: Optional[str]
    city: Optional[str]
    state: Optional[str]
    zip: Optional[int]
    phone: str
    email: EmailStr
    referring: Optional[str]
    conditions: list[str]
    otherCondition: Optional[str]
    diseases: list[str]
    medications: str
    covidTestedPositive: Optional[bool] or None
    covidVaccine: Optional[bool] or None
    stressfulLevel: int
    consentMinorChild: Optional[bool]
    relationshipChild: Optional[str]


class Client(BaseModel):
    api_key: Optional[str]
    first_name: str
    last_name: str
    phone: str
    email: str

    class Config:
        orm_mode = True


class ClientPhone(BaseModel):
    phone: str

    class Config:
        orm_mode = True
