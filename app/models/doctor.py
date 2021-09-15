import enum
from uuid import uuid4

from sqlalchemy import Enum

from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base


def gen_uuid() -> str:
    return str(uuid4())


class Doctor(Base):
    __tablename__ = "doctors"

    class DoctorRole(enum.Enum):
        ADMIN = "ADMIN"
        DOCTOR = "DOCTOR"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(64))
    last_name = Column(String(64))
    email = Column(String(128), unique=True, index=True)
    email_approved = Column(Boolean, default=True)
    hash_password = Column(String)
    role = Column(Enum(DoctorRole), default=DoctorRole.DOCTOR.value)
    api_key = Column(String(128), default=gen_uuid)

    def __repr__(self):
        return f"<{self.id}: {self.email}>"

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"
