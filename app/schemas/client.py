import datetime
from pydantic import BaseModel


class Client(BaseModel):
    first_name: str
    last_name: str
    dateBirth: datetime.datetime
    address: str
    city: str
    state: str
    zip: int
    phone: int
    email: str
    conditions: str
    otherLabel: str
    checkboxesFollowing: str
    medications: str
    testedPositive: str
    covidVaccine: str
    stressfulLevel: str
    consentMinorChild: str
    relationshipChild: str

    class Config:
        orm_mode = True


class ClientCreate(BaseModel):
    first_name: str
    last_name: str
    phone: int
    email: str

    class Config:
        orm_mode = True
