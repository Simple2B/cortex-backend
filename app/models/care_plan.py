import datetime

from sqlalchemy import Column, ForeignKey, Integer, DateTime, String
from sqlalchemy.orm import relationship

from app.database import Base
from .utils import ModelMixin


class CarePlan(Base, ModelMixin):
    __tablename__ = "careplans"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime, default=datetime.datetime.today)
    care_plan = Column(String(128), nullable=True)
    frequency = Column(String(128), nullable=True)
    progress_date = Column(DateTime, nullable=True)

    client_id = Column(Integer, ForeignKey("clients.id"))
    doctor_id = Column(Integer, ForeignKey("doctors.id"))

    client = relationship("Client", viewonly=True)
    doctor = relationship("Doctor", viewonly=True)

    def __repr__(self):
        return f"<{self.id}: c:{self.client_id}-d:{self.doctor_id}>"

    @property
    def care_plan_info(self):
        from .test import Test

        tests = Test.query.filter(Test.care_plan_id == self.id).all()

        return tests
