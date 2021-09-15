from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base


class Queue(Base):
    __tablename__ = "queues"

    id = Column(Integer, primary_key=True, index=True)
    place_in_queue = Column(Integer)
    canceled = Column(Boolean, default=False)

    client_id = Column(Integer, ForeignKey("clients.id"))
    visit_id = Column(Integer, nullable=True)
    reception_id = Column(Integer, ForeignKey("receptions.id"))

    # clients = relationship("Client", viewonly=True)
    reception = relationship("Reception")
