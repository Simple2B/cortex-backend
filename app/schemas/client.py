import datetime
from pydantic import BaseModel, EmailStr
from sqlalchemy.sql.sqltypes import Integer


class ClientInfo(BaseModel):
    first_name: str
    last_name: str
    birthday: datetime.date
    address: str
    city: str
    state: str
    zip: int
    phone: str
    email: EmailStr
    conditions: list[str]
    other_condition: str or None
    diseases: list[str]
    medications: str
    covid_tested_positive: bool or None
    covid_vaccine: bool or None
    stressful_level: int
    consent_minor_child: bool
    relationship_child: str or None


class Client(BaseModel):
    api_key: str
    first_name: str
    last_name: str
    phone: str
    email: str

    class Config:
        orm_mode = True
