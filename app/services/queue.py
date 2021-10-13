import datetime

from app.schemas import Client, Doctor, ClientPhone
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
            log(log.ERROR, "add_client_to_queue: Client doesn't registration")
        reception = Reception.query.filter(Reception.doctor_id == doctor.id).first()
        reception.date = datetime.datetime.now()
        reception.save()
        log(log.INFO, "add_client_to_queue: Reception created [%d]", reception.id)
        visit = Visit.query.filter(Visit.client_id == client.id).first()
        if not visit:
            visit = Visit(
                data_time=datetime.datetime.now(),
                # TODO duration => may be end of visit
                # TODO rougue_mode=,
                client_id=client.id,
                doctor_id=doctor.id,
            )
            visit.save()
            log(log.INFO, "add_client_to_queue: Visit created [%d]", visit.id)
        else:
            # TODO duration => may be end of visit
            # TODO visit.rougue_mode=,
            visit.data_time = datetime.datetime.now()
            visit.doctor_id = doctor.id
            visit.save()
        client_in_queue = QueueMember.query.all()

        place_in_queue = None
        if len(client_in_queue) > 0:
            place_in_queue = len(client_in_queue) + 1
        else:
            place_in_queue = 1

        queue_member = QueueMember(
            client_id=client.id,
            visit_id=visit.id,
            reception_id=reception.id,
            place_in_queue=place_in_queue,
        )
        queue_member.save()
        log(log.INFO, "add_client_to_queue: QueueMember created [%d]", queue_member.id)

    def identify_client_with_phone(
        self, phone_num: ClientPhone, doctor: Doctor
    ) -> Client:
        client = ClientDB.query.filter(ClientDB.phone == phone_num.phone).first()
        if not client:
            log(
                log.ERROR,
                "identify_client_with_phone: No such phone number [%s] Client doesn't registration",
                phone_num.phone,
            )
        self.add_client_to_queue(client, doctor)
        return client
