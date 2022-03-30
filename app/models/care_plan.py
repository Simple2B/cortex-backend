import datetime

from sqlalchemy import Column, ForeignKey, Integer, DateTime, String
from sqlalchemy.orm import relationship

from app.database import Base
from .utils import ModelMixin

time = datetime.datetime.utcnow().strftime("%m/%d/%Y, %H:%M:%S")


class CarePlan(Base, ModelMixin):
    __tablename__ = "careplans"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime, default=datetime.datetime.today)

    start_time = Column(
        DateTime, default=datetime.datetime.strptime(time, "%m/%d/%Y, %H:%M:%S")
    )
    end_time = Column(DateTime, nullable=True)

    care_plan = Column(String(128), nullable=True)
    frequency = Column(String(128), nullable=True)
    progress_date = Column(DateTime, nullable=True)

    client_id = Column(Integer, ForeignKey("clients.id"))
    doctor_id = Column(Integer, ForeignKey("doctors.id"))

    client = relationship("Client", viewonly=True)
    doctor = relationship("Doctor", viewonly=True)

    def __repr__(self):
        return f"<{self.id}: c:{self.client_id}-d:{self.doctor_id}>"

    @property
    def care_plan_info_tests(self):
        from .test import Test
        from .visit import Visit

        tests = Test.query.filter(Test.care_plan_id == self.id).all()

        # notes in visit
        visits = Visit.query.filter(Visit.client_id == self.client_id).all()

        care_plan_visit = []
        if len(visits) > 0:
            for visit in visits:
                if self.end_time and visit.end_time:
                    if (
                        self.start_time >= visit.start_time
                        and self.end_time <= visit.end_time
                    ):
                        care_plan_visit.append(visit)

        # intake consult
        return {
            "tests": tests,
            "visits": visits,
        }
