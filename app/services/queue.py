import datetime

from fastapi import HTTPException, status
from sqlalchemy import and_
from app.schemas import Client, Doctor, ClientPhone
from app.models import (
    QueueMember,
    Reception,
    Client as ClientDB,
    Doctor as DoctorDB,
)

from app.logger import log


class QueueService:
    def add_client_to_queue(self, client_data: Client, doctor: Doctor):
        client = ClientDB.query.filter(ClientDB.phone == client_data.phone).first()
        if not client:
            log(log.ERROR, "add_client_to_queue: Client doesn't registration")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Client not found"
            )
        reception = Reception.query.filter(
            and_(
                Reception.doctor_id == doctor.id,
                Reception.date == datetime.date.today(),
            )
        ).first()

        if not reception:
            reception = Reception(
                date=datetime.date.today(),
                doctor_id=doctor.id,
            )
            reception.save(True)

            log(log.INFO, "add_client_to_queue: Reception created [%d]", reception.id)

        client_in_queue = QueueMember.query.filter(
            QueueMember.reception_id == reception.id
        ).all()

        place_in_queue = len(client_in_queue) + 1 if client_in_queue else 1

        log(log.INFO, "add_client_to_queue: place_in_queue [%d]", place_in_queue)

        queue_member = QueueMember(
            client_id=client.id,
            reception_id=reception.id,
            place_in_queue=place_in_queue,
            canceled=False,
        )
        queue_member.save(True)
        log(log.INFO, "add_client_to_queue: QueueMember created [%d]", queue_member.id)

    def delete_client_from_queue(self, client_data: Client, doctor: Doctor) -> None:
        client: ClientDB = ClientDB.query.filter(
            ClientDB.phone == client_data.phone
        ).first()

        if not client:
            log(log.ERROR, "delete_client_from_queue: Client doesn't registration")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Client not found"
            )

        log(
            log.INFO,
            "delete_client_from_queue: Client [%d] [%s] from db",
            client.id,
            client.first_name,
        )

        reception: Reception = Reception.query.filter(
            and_(
                Reception.doctor_id == doctor.id,
                Reception.date == datetime.date.today(),
            )
        ).first()

        if not reception:
            log(
                log.ERROR,
                "delete_client_from_queue: reception doesn't found [%s]",
                reception.id,
            )
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Reception not found"
            )

        log(log.INFO, "delete_client_from_queue: reception today [%s]", reception.id)

        queue_member: QueueMember = QueueMember.query.filter(
            and_(
                QueueMember.reception_id == reception.id,
                QueueMember.client_id == client.id,
            )
        ).first()

        if not queue_member:
            log(
                log.WARNING,
                "Not found query_member for client [%d], reception [%d]",
                client.id,
                reception.id,
            )
            return

        queue_member.canceled = True
        queue_member.save()

        log(
            log.INFO,
            "delete_client_from_queue: queue_member [%s] deleted",
            queue_member,
        )

    def identify_client_with_phone(
        self, phone_num: ClientPhone, doctor: Doctor
    ) -> Client:
        doctor = DoctorDB.query.filter(DoctorDB.email == doctor.email).first()
        client = ClientDB.query.filter(ClientDB.phone == phone_num.phone).first()
        if not client:
            log(
                log.ERROR,
                "identify_client_with_phone: No such phone number [%s] Client doesn't registration",
                phone_num.phone,
            )
        self.add_client_to_queue(client, doctor)
        return client

    def get_client_with_phone(phone: str) -> Client:
        client = ClientDB.query.filter(ClientDB.phone == phone).first()
        if not client:
            log(
                log.ERROR,
                "identify_client_with_phone: No such phone number [%s] Client doesn't registration",
                phone,
            )
        return client
