import datetime

from sqlalchemy import Column, ForeignKey, Integer, Date, String
from sqlalchemy.orm import relationship

from app.database import Base
from .utils import ModelMixin


class Note(Base, ModelMixin):
    __tablename__ = "notes"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, default=datetime.date.today)
    notes = Column(String(128))

    client_id = Column(Integer, ForeignKey("clients.id"))
    doctor_id = Column(Integer, ForeignKey("doctors.id"))
    visit_id = Column(Integer, ForeignKey("visits.id"))

    client = relationship("Client", viewonly=True)
    doctor = relationship("Doctor", viewonly=True)
    visit = relationship("Visit", viewonly=True)

    def __repr__(self):
        return f"<Note:{self.id}: c:{self.client_id}-d:{self.doctor_id}>"
