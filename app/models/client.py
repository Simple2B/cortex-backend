from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
from app.database import Base


class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(64))
    last_name = Column(String(64))
    date_of_birthday = Column(DateTime(timezone=True), nullable=True)
    address = Column(String(128), nullable=True)
    city = Column(String(64))
    state = Column(String(64))
    zip = Column(Integer)

    phone_num = Column(String(32), unique=True, index=True)
    email = Column(String(128), unique=True, index=True)

    queue_id = Column(Integer, ForeignKey("queues.id"))
    doctor_id = Column(Integer, ForeignKey("doctors.id"))

    queue = relationship("Queue")
    doctor = relationship("Doctor")

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"
