import datetime
from sqlalchemy import Date, Column, ForeignKey, Integer
from sqlalchemy.orm import relationship
from app.database import Base
from .utils import ModelMixin


class Reception(Base, ModelMixin):
    __tablename__ = "receptions"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, default=datetime.date.today)
    doctor_id = Column(Integer, ForeignKey("doctors.id"))

    doctor = relationship("Doctor", viewonly=True)
    queue_members = relationship("QueueMember", viewonly=True)
