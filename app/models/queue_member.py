from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base
from .utils import ModelMixin


class QueueMember(Base, ModelMixin):
    __tablename__ = "queue_members"

    id = Column(Integer, primary_key=True, index=True)
    place_in_queue = Column(Integer)
    canceled = Column(Boolean, default=False)

    client_id = Column(Integer, ForeignKey("clients.id"))
    visit_id = Column(Integer, nullable=True)
    reception_id = Column(Integer, ForeignKey("receptions.id"))

    client = relationship("Client", viewonly=True)
    reception = relationship("Reception", viewonly=True)
