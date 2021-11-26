import datetime

from sqlalchemy import Column, ForeignKey, Integer, DateTime, String
from sqlalchemy.orm import relationship

from app.database import Base
from .utils import ModelMixin


class Test(Base, ModelMixin):
    __tablename__ = "tests"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime, default=datetime.datetime.today)

    client_id = Column(Integer, ForeignKey("clients.id"))
    doctor_id = Column(Integer, ForeignKey("doctors.id"))

    care_plan = Column(String(128), nullable=True)
    frequency = Column(String(128), nullable=True)

    client = relationship("Client", viewonly=True)
    doctor = relationship("Doctor", viewonly=True)

    def __repr__(self):
        return f"<{self.id}: c:{self.client_id}-d:{self.doctor_id}>"
