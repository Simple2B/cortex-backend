from sqlalchemy import Column, Integer, String, DateTime
from app.database import Base
from .utils import ModelMixin


class Client(Base, ModelMixin):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(64), nullable=False)
    last_name = Column(String(64), nullable=False)
    dateBirth = Column(DateTime(timezone=True), nullable=True)
    address = Column(String(128), nullable=True)
    city = Column(String(64), nullable=True)
    state = Column(String(64), nullable=True)
    zip = Column(Integer, nullable=True)

    phone = Column(String(32), unique=True, index=True)
    email = Column(String(128), unique=True, index=True)

    # checkBoxesСonditions:
    conditions = Column(String, nullable=False)
    otherLabel = Column(String, nullable=True)

    # following
    checkboxesFollowing = Column(String, nullable=True)

    medications = Column(String, nullable=True)
    testedPositive = Column(String, nullable=True)
    covidVaccine = Column(String, nullable=True)
    stressfulLevel = Column(String, nullable=False)
    consentMinorChild = Column(String, nullable=True)
    relationshipChild = Column(String, nullable=True)

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"
