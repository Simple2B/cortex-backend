import datetime

from sqlalchemy import Boolean, Column, ForeignKey, Integer, DateTime, Date
from sqlalchemy.orm import relationship

from app.database import Base
from .utils import ModelMixin

time = datetime.datetime.utcnow().strftime("%m/%d/%Y, %H:%M:%S")


class Test(Base, ModelMixin):
    __tablename__ = "tests"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(
        DateTime, default=datetime.datetime.strptime(time, "%m/%d/%Y, %H:%M:%S")
    )

    client_id = Column(Integer, ForeignKey("clients.id"))
    doctor_id = Column(Integer, ForeignKey("doctors.id"))

    client = relationship("Client", viewonly=True)
    doctor = relationship("Doctor", viewonly=True)

    def __repr__(self):
        return f"<{self.id}: c:{self.client_id}-d:{self.doctor_id}>"
