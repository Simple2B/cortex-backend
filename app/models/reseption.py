from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base


class Reseption(Base):
    __tablename__ = "reseptions"

    id = Column(Integer, primary_key=True, index=True)
    date =
    doctor_id =
