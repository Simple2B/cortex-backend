import enum
from pydantic import BaseModel, EmailStr
from typing import Optional


class YesNoNone(enum.Enum):
    YES = "yes"
    NO = "no"
    NONE = "null"


class ClientInfo(BaseModel):
    id: Optional[int]
    api_key: Optional[str]
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
    covidTestedPositive: Optional[YesNoNone]
    covidVaccine: Optional[YesNoNone]
    stressfulLevel: int
    consentMinorChild: Optional[bool]
    relationshipChild: Optional[str]

    class Config:
        orm_mode = True


class Client(BaseModel):
    id: Optional[int]
    api_key: Optional[str]
    first_name: str
    last_name: str
    phone: str
    email: str

    class Config:
        orm_mode = True


class ClientInTake(BaseModel):
    api_key: str
    rougue_mode: bool


class ClientPhone(BaseModel):
    phone: str

    class Config:
        orm_mode = True
