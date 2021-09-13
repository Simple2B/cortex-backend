from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base


class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(64))
    phon_num = Column(String(128), unique=True, index=True)

    doctor_id = Column(Integer, ForeignKey("doctors.id"))

    doctor = relationship("Doctor")
