import datetime
from pydantic import BaseModel, EmailStr


class ClientInfo(BaseModel):
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
    otherCondition: str or None
    diseases: list[str]
    medications: str
    covidTestedPositive: bool or None
    covidVaccine: bool or None
    stressfulLevel: int
    consentMinorChild: bool
    relationshipChild: str or None


class Client(BaseModel):
    api_key: str
    first_name: str
    last_name: str
    phone: str
    email: str

    class Config:
        orm_mode = True
