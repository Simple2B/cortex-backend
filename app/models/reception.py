from datetime import datetime
from sqlalchemy import DateTime, Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base


class Reception(Base):
    __tablename__ = "receptions"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime, default=datetime.utcnow)
    doctor_id = Column(Integer, ForeignKey("doctors.id"))

    doctors = relationship("Doctor", viewonly=True)
    queue = relationship("Queue")
