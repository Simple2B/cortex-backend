import datetime

from app.schemas import Client, Doctor
from app.models import (
    QueueMember,
    Reception,
    Visit,
    Client as ClientDB,
    Doctor as DoctorDB,
)

from app.logger import log


class QueueService:
    def add_client_to_queue(self, client_data: Client, doctor: Doctor) -> Client:

        doctor = DoctorDB.query.filter(DoctorDB.email == doctor.email).first()

        client = ClientDB.query.filter(ClientDB.phone == client_data.phone).first()

        if not client:
            return

        reception = Reception.query.filter(Reception.doctor_id == doctor.id).first()
        reception.date = datetime.datetime.now()

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
