import datetime

from sqlalchemy import Column, ForeignKey, Integer, DateTime, String
from sqlalchemy.orm import relationship

from app.database import Base
from .utils import ModelMixin


class Billing(Base, ModelMixin):
    __tablename__ = "billings"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime, default=datetime.datetime.today)

    description = Column(String(128), nullable=True)
    amount = Column(Integer, nullable=False)

    customer_stripe_id = Column(String(128), nullable=True)
    subscription_id = Column(String(128), nullable=True)
    subscription_quantity = Column(Integer, nullable=True)
    subscription_interval = Column(String(128), nullable=True)
    subscription_interval_count = Column(Integer, nullable=True)
    payment_method = Column(String(128), nullable=True)
    status = Column(String(32), nullable=True)

    client_id = Column(Integer, ForeignKey("clients.id"))
    doctor_id = Column(Integer, ForeignKey("doctors.id"))

    client = relationship("Client", viewonly=True)
    doctor = relationship("Doctor", viewonly=True)

    def __repr__(self):
        return f"<{self.id}: c:{self.client_id}-d:{self.doctor_id}>"
