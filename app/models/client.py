from uuid import uuid4
from sqlalchemy.orm import relationship
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

    medications = Column(String(128), nullable=True)
    covid_tested_positive = Column(Boolean, nullable=True, default=None)
    covid_vaccine = Column(Boolean, nullable=True, default=None)
    stressful_level = Column(Integer)
    consent_minor_child = Column(Boolean, default=False)
    relationship_child = Column(String, nullable=True, default=None)

    api_key = Column(String(36), default=gen_uuid)

    def __str__(self) -> str:
        return f"{self.id}: {self.first_name} {self.last_name}"
