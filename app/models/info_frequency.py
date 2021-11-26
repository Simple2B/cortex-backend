from sqlalchemy import Column, Integer, String

from app.database import Base
from .utils import ModelMixin


class InfoFrequency(Base, ModelMixin):
    __tablename__ = "info_frequencies"

    id = Column(Integer, primary_key=True, index=True)
    frequency = Column(String(128), nullable=True)

    def __repr__(self):
        return f"<{self.id}: c:{self.frequency}>"
