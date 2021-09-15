from datetime import datetime
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
from app.database import Base


class Visit(Base):
    __tablename__ = "visits"

    id = Column(Integer, primary_key=True, index=True)
    data_time = Column(DateTime, default=datetime.utcnow)
    # ? duration => may be end of visit
    rougue_mode = Column(Boolean, default=False)

    client_id = Column(Integer, ForeignKey("clients.id"))
    doctor_id = Column(Integer, ForeignKey("doctors.id"))

    client = relationship("Client", viewonly=True)
    doctor = relationship("Doctor", viewonly=True)

    def __repr__(self):
        return f"<{self.id}: c:{self.client_id}-d:{self.doctor_id}>"
