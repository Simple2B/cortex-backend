import datetime

# from .auth import get_current_doctor
from app.schemas import Client, ClientInfo
from app.models import QueueMember, Reception, Doctor, Visit

# from app.logger import log


class QueueService:
    def add_client_to_queue(self, client_data: ClientInfo) -> Client:

        doctor = Doctor.query.first()

        # if current_user.is_authenticated():
        #     doctor_id = current_user.get_id()

        # doctors = Doctor.query.all()
        # for i in doctors:
        #     doctor = doctors[i]
        #     doctor: Doctor = current_user
        #     if doctor.is_authenticated:
        #         return doctor

        # client = ClientDB.query.filter(ClientDB.phone == client_data.phone).first

        reception = Reception(
            date=datetime.datetime.now(),
            doctor_id=doctor.id,
        )

        reception.save()

        visit = Visit(
            data_time=datetime.datetime.now(),
            # ? duration => may be end of visit
            # rougue_mode=,
            client_id=client_data.id,
            doctor_id=doctor.id,
        )
        visit.save()

        queue_member = QueueMember(
            # place_in_queue=,
            # canceled=,
            client_id=client_data.id,
            visit_id=visit.id,
            reception_id=reception.id,
        )

        queue_member.save()

        # return queue_member
