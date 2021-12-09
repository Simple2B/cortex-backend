from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base
from .utils import ModelMixin


class Condition(Base, ModelMixin):
    __tablename__ = "conditions"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(64))

    def __str__(self) -> str:
        return f"{self.id} {self.name}"


class ClientCondition(Base, ModelMixin):
    __tablename__ = "client_conditions"

    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("clients.id"))
    condition_id = Column(Integer, ForeignKey("conditions.id"))

    condition = relationship("Condition", viewonly=True)

    def __str__(self) -> str:
        return f"{self.id}"
