from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base


class Quene(Base):
    __tablename__ = "quenes"

    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, unique=True)
    reseption_id = Column(Integer, unique=True)
    place_in_quene = Column(Integer)
    visit_id = Column(Integer, nullable=True)

    clients = relationship("Client", viewonly=True)
