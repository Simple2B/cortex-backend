from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base


class Quene(Base):
    __tablename__ = "quenes"

    id = Column(Integer, primary_key=True, index=True)
    client_id =
    reseption_id =
    place_in_quene =
    visit_id = (null)
