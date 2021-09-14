from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base


class Queue(Base):
    __tablename__ = "queues"

    id = Column(Integer, primary_key=True, index=True)
    place_in_queue = Column(Integer)

    client_id = Column(Integer, ForeignKey("clients.id"))
    visit_id = Column(Integer, ForeignKey("visit.id"))
    reception_id = Column(Integer, ForeignKey("reception.id"))

    clients = relationship("Client", viewonly=True)
    visits = relationship("Visit", viewonly=True)
    reception = relationship("Reception")
