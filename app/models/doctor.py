import enum
from uuid import uuid4

from sqlalchemy import Enum

from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy import func
from sqlalchemy.ext.hybrid import hybrid_property
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import AnonymousUserMixin, UserMixin
from app.database import Base
from .utils import ModelMixin


def gen_uuid() -> str:
    return str(uuid4())


class Doctor(Base, ModelMixin, UserMixin):
    __tablename__ = "doctors"

    class DoctorRole(enum.Enum):
        ADMIN = "ADMIN"
        DOCTOR = "DOCTOR"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(64))
    last_name = Column(String(64))
    email = Column(String(128), unique=True, index=True)
    email_approved = Column(Boolean, default=True)
    hash_password = Column(String(255), nullable=True)
    role = Column(Enum(DoctorRole), default=DoctorRole.DOCTOR.value)
    api_key = Column(String(128), default=gen_uuid)

    def __repr__(self):
        return f"<{self.id}: {self.email}>"

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"

    @hybrid_property
    def password(self):
        return self.hash_password

    @password.setter
    def password(self, password):
        self.hash_password = generate_password_hash(password)

    @classmethod
    def authenticate(cls, email, password):
        doctor = cls.query.filter(func.lower(cls.email) == func.lower(email)).first()
        if doctor is not None and check_password_hash(doctor.password, password):
            return doctor


class AnonymousUser(AnonymousUserMixin):
    pass
