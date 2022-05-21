from datetime import datetime, date

from sqlalchemy import Column, ForeignKey, Integer, DateTime, String
from sqlalchemy.orm import relationship

from app.database import Base
from .utils import ModelMixin

# from app.logger import log

time = datetime.utcnow().strftime("%m/%d/%Y, %H:%M:%S")


class CarePlan(Base, ModelMixin):
    __tablename__ = "careplans"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime, default=date.today)

    start_time = Column(DateTime, default=datetime.strptime(time, "%m/%d/%Y, %H:%M:%S"))
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
        from .note import Note
        from .consult import Consult

        tests = Test.query.filter(Test.care_plan_id == self.id).all()
        visits = Visit.query.filter(Visit.client_id == self.client_id).all()

        care_plan_visits_with_end_date = []
        care_plan_visits_without_end_date = []

        if len(visits) > 0:
            for visit in visits:
                if self.end_time and visit.end_time:
                    if (
                        self.start_time.date()
                        <= visit.start_time.date()
                        <= visit.end_time.date()
                    ):
                        care_plan_visits_with_end_date.append(visit)
                if self.end_time and not visit.end_time:
                    if self.start_time <= visit.start_time:
                        care_plan_visits_without_end_date.append(visit)

        notes = Note.query.filter(Note.client_id == self.client_id).all()

        care_plan_notes = []

        if len(notes) > 0:
            for note in notes:
                if self.end_time:
                    if self.end_time.date() >= note.date:
                        care_plan_notes.append(note)
                if not self.end_time:
                    if self.start_time.date() <= note.date:
                        care_plan_notes.append(note)

        consults = Consult.query.filter(Consult.client_id == self.client_id).all()

        care_plan_consults = []

        if len(consults) > 0:
            for consult in consults:
                if self.end_time:
                    if self.end_time.date() >= consult.date:
                        care_plan_consults.append(consult)
                if not self.end_time:
                    if self.start_time.date() <= consult.date:
                        care_plan_consults.append(consult)

        return {
            "tests": tests,
            "visits_with_end_date": care_plan_visits_with_end_date,
            "visits_without_end_date": care_plan_visits_without_end_date,
            "notes": care_plan_notes,
            "consults": care_plan_consults,
        }
