import datetime

# from .auth import get_current_doctor
from app.schemas import Client, ClientInfo
from app.models import QueueMember, Reception, Doctor, Visit, Client as ClientDB

from app.logger import log


class QueueService:
    def add_client_to_queue(self, client_data: Client) -> Client:

        doctor = Doctor.query.first()

        # if current_user.is_authenticated():
        #     doctor_id = current_user.get_id()

        # doctors = Doctor.query.all()
        # for i in doctors:
        #     doctor = doctors[i]
        #     doctor: Doctor = current_user
        #     if doctor.is_authenticated:
        #         return doctor

        client = ClientDB.query.filter(ClientDB.phone == client_data.phone).first()

        if not client:
            return

        reception = Reception.query.filter(Reception.doctor_id == doctor.id).first()
        reception.date = datetime.datetime.now()

        # reception = Reception(
        #     date=datetime.datetime.now(),
        #     doctor_id=doctor.id,
        # )

        reception.save()

        log(log.INFO, "Reception created [%d]", reception.id)

        visit = Visit.query.filter(Visit.client_id == client.id).first()
        if not visit:
            visit = Visit(
                data_time=datetime.datetime.now(),
                # ? duration => may be end of visit
                # rougue_mode=,
                client_id=client.id,
                doctor_id=doctor.id,
            )
            visit.save()

            log(log.INFO, "Visit created [%d]", visit.id)
        else:
            # ? duration => may be end of visit
            # visit.rougue_mode=,
            visit.data_time = datetime.datetime.now()
            visit.doctor_id = doctor.id

            visit.save()

        queue_member = QueueMember(
            # place_in_queue=,
            # canceled=,
            client_id=client.id,
            visit_id=visit.id,
            reception_id=reception.id,
        )

        queue_member.save()

        log(log.INFO, "QueueMember created [%d]", queue_member.id)

        # return queue_member
