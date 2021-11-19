import enum
from pydantic import BaseModel, EmailStr
from typing import Optional

from .utils import OrmModeModel


class YesNoNone(enum.Enum):
    YES = "yes"
    NO = "no"
    NONE = "null"


class ClientInfo(OrmModeModel):
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
    visits: Optional[list]


class Client(OrmModeModel):
    id: Optional[int]
    api_key: Optional[str]
    first_name: str
    last_name: str
    phone: str
    email: str
    rougue_mode: Optional[bool]


class ClientQueue(Client):
    place_in_queue: Optional[int]


class ClientInTake(BaseModel):
    api_key: str
    place_in_queue: Optional[int]
    rougue_mode: Optional[bool]


class ClientPhone(OrmModeModel):
    phone: str
