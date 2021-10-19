from uuid import uuid4
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.sql.sqltypes import Boolean
from app.database import Base
from .utils import ModelMixin


def gen_uuid() -> str:
    return str(uuid4())


class Client(Base, ModelMixin):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(64), nullable=False)
    last_name = Column(String(64), nullable=False)
    birthday = Column(Date, nullable=True)
    address = Column(String(128), nullable=True)
    city = Column(String(64), nullable=True)
    state = Column(String(64), nullable=True)
    zip = Column(Integer, nullable=True)
    phone = Column(String(32), unique=True, index=True)
    email = Column(String(128), unique=True, index=True)
    referring = Column(String(128), nullable=True)
    medications = Column(String(128), nullable=True)
    covid_tested_positive = Column(String, default="null")
    covid_vaccine = Column(String, default="null")
    stressful_level = Column(Integer)
    consent_minor_child = Column(Boolean, default=False)
    relationship_child = Column(String, nullable=True, default=None)

    api_key = Column(String(36), default=gen_uuid)

    def __str__(self) -> str:
        return f"{self.id}: {self.first_name} {self.last_name}"

    def __repr__(self) -> str:
        return self.__str__()

    @property
    def client_info(self):
        from .condition import ClientCondition
        from .disease import ClientDisease

        conditions = [
            link.condition.name
            for link in ClientCondition.query.filter(
                ClientCondition.client_id == self.id
            ).all()
        ]

        diseases = [
            link.disease.name
            for link in ClientDisease.query.filter(
                ClientDisease.client_id == self.id
            ).all()
        ]

        if self.covid_tested_positive == "true":
            self.covid_tested_positive = "yes"
        elif self.covid_tested_positive == "false":
            self.covid_tested_positive = "no"
        else:
            "null"

        if self.covid_vaccine == "true":
            self.covid_vaccine = "yes"
        elif self.covid_vaccine == "false":
            self.covid_vaccine = "no"
        else:
            "null"

        return {
            "id": self.id,
            "api_key": self.api_key,
            "firstName": self.first_name,
            "lastName": self.last_name,
            "birthday": self.birthday.strftime("%m/%d/%Y"),
            "address": self.address,
            "city": self.city,
            "state": self.state,
            "zip": self.zip,
            "phone": self.phone,
            "email": self.email,
            "referring": self.referring,
            "conditions": conditions,
            "otherCondition": "",
            "diseases": diseases,
            "medications": self.medications,
            "covidTestedPositive": self.covid_tested_positive,
            "covidVaccine": self.covid_vaccine,
            "stressfulLevel": self.stressful_level,
            "consentMinorChild": self.consent_minor_child,
            "relationshipChild": self.relationship_child,
        }
