import datetime
from pydantic import BaseModel, EmailStr
from typing import Optional


class ClientInfo(BaseModel):
    id: int
    firstName: str
    lastName: str
    birthday: datetime.date
    address: str
    city: str
    state: str
    zip: int
    phone: str
    email: EmailStr
    referring: str
    conditions: list[str]
    otherCondition: Optional[str]
    diseases: list[str]
    medications: str
    covidTestedPositive: Optional[bool]
    covidVaccine: Optional[bool]
    stressfulLevel: int
    consentMinorChild: bool
    relationshipChild: Optional[str]

    # tags: List[str] = []


class Client(BaseModel):
    api_key: str
    first_name: str
    last_name: str
    phone: str
    email: str

    class Config:
        orm_mode = True
