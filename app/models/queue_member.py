from sqlalchemy import Boolean, Column, ForeignKey, Integer
from sqlalchemy.orm import relationship

from app.database import Base
from .utils import ModelMixin


class QueueMember(Base, ModelMixin):
    __tablename__ = "queue_members"

    id = Column(Integer, primary_key=True, index=True)
    place_in_queue = Column(Integer, nullable=True)
    canceled = Column(Boolean, default=False)

    client_id = Column(Integer, ForeignKey("clients.id"))
    visit_id = Column(Integer, nullable=True)
    reception_id = Column(Integer, ForeignKey("receptions.id"))

    client = relationship("Client", viewonly=True)
    reception = relationship("Reception", viewonly=True)

    def __str__(self) -> str:
        return f"client {self.client_id}: [{self.client}]"

    def __repr__(self) -> str:
        return self.__str__()
