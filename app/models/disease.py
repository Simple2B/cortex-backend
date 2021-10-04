from sqlalchemy import Column, Integer, String, ForeignKey
from app.database import Base
from .utils import ModelMixin


class Disease(Base, ModelMixin):
    __tablename__ = "diseases"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(64))

    def __str__(self) -> str:
        return f"{self.id} {self.name}"


class ClientDisease(Base, ModelMixin):
    __tablename__ = "client_diseases"

    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("clients.id"))
    disease_id = Column(Integer, ForeignKey("diseases.id"))
