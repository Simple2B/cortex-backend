import datetime
from sqlalchemy import Boolean, Column, ForeignKey, Integer, DateTime, Date, String
from sqlalchemy.orm import relationship
from app.database import Base
from .utils import ModelMixin

time = datetime.datetime.utcnow().strftime("%m/%d/%Y, %H:%M:%S")


class Visit(Base, ModelMixin):
    __tablename__ = "visits"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, default=datetime.date.today())
    start_time = Column(
        DateTime, default=datetime.datetime.strptime(time, "%m/%d/%Y, %H:%M:%S")
    )
    end_time = Column(DateTime, nullable=True)
    rougue_mode = Column(Boolean, default=False)

    client_id = Column(Integer, ForeignKey("clients.id"))
    doctor_id = Column(Integer, ForeignKey("doctors.id"))

    client = relationship("Client", viewonly=True)
    doctor = relationship("Doctor", viewonly=True)

    def __repr__(self):
        return f"<{self.id}: c:{self.client_id}-d:{self.doctor_id}>"

    @property
    def visit_info(self):

        return {
            "id": self.id,
            "date": self.date,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "client_info": self.client.client_info,
            # TODO: add doctor when doctor would be not one
            # "doctor": self.doctor,
        }
