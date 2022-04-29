from sqlalchemy import ForeignKey, Column, Integer, String

from app.database import Base
from .utils import ModelMixin

from sqlalchemy.orm import relationship


class InfoCarePlan(Base, ModelMixin):
    __tablename__ = "info_care_plans"

    id = Column(Integer, primary_key=True, index=True)
    care_plan = Column(String(128), nullable=True)

    doctor_id = Column(Integer, ForeignKey("doctors.id"))
    client_id = Column(Integer, ForeignKey("clients.id"))

    doctor = relationship("Doctor", viewonly=True)
    client = relationship("Client", viewonly=True)

    def __repr__(self):
        return f"<{self.id}: c:{self.care_plan}>"
