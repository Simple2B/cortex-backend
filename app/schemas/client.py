import datetime
import enum
from pydantic import BaseModel, EmailStr
from typing import Optional


class YesNoNone(enum.Enum):
    YES = "yes"
    NO = "no"
    NONE = "null"


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
    covidTestedPositive: Optional[YesNoNone]
    covidVaccine: Optional[YesNoNone]
    stressfulLevel: int
    consentMinorChild: Optional[bool]
    relationshipChild: Optional[str]

    class Config:
        orm_mode = True


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


class ClientIntake(BaseModel):
    api_key: Optional[str]
    firstName: Optional[str]
    lastName: Optional[str]
    birthday: Optional[datetime.date]
    address: Optional[str]
    city: Optional[str]
    state: Optional[str]
    zip: Optional[int]
    phone: Optional[str]
    email: EmailStr
    referring: Optional[str]
    # conditions: list[str]
    otherCondition: Optional[str]
    # diseases: list[str]
    medications: Optional[str]
    covidTestedPositive: Optional[YesNoNone]
    covidVaccine: Optional[YesNoNone]
    stressfulLevel: Optional[int]
    consentMinorChild: Optional[bool]
    relationshipChild: Optional[str]

    class Config:
        orm_mode = True
