import datetime
import re
from typing import List, Union

from fastapi import HTTPException, status
from sqlalchemy import and_

from app.schemas import Client, Doctor, ClientQueue
from app.models import (
    QueueMember,
    Reception,
    Client as ClientDB,
    Doctor as DoctorDB,
    CarePlan,
    Test,
)
from app.logger import log


class QueueService:
    def add_client_to_queue(self, client_data: Client, doctor: Doctor):
        client = ClientDB.query.filter(ClientDB.phone == client_data.phone).first()
        if not client:
            log(
                log.ERROR,
                "add_client_to_queue: Client [%s] is not registered",
                client_data.phone,
            )
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Client not found"
            )

        today = datetime.date.today()
        reception = Reception.query.filter(
            and_(
                Reception.doctor_id == doctor.id,
                Reception.date == today,
            )
        ).first()

        if not reception:
            reception = Reception(
                date=today,
                doctor_id=doctor.id,
            )
            reception.save()

            log(log.INFO, "add_client_to_queue: Reception created [%d]", reception.id)

        clients_in_queue = QueueMember.query.filter(
            QueueMember.reception_id == reception.id
        ).all()

        # list({member["id"]: member for member in clients_in_queue}.values())

        for i in range(len(clients_in_queue)):
            clients_in_queue[i].place_in_queue = i + 1
            clients_in_queue[i].save()
            if (
                clients_in_queue[i].canceled is False
                and clients_in_queue[i].client_id == client.id
            ):
                log(
                    log.INFO,
                    "add_client_to_queue: this client in queue still [%s]",
                    client,
                )
                return

        place_in_queue = len(clients_in_queue) + 1 if clients_in_queue else 1

        log(log.INFO, "add_client_to_queue: place_in_queue [%d]", place_in_queue)

        queue_member = QueueMember(
            client_id=client.id,
            reception_id=reception.id,
            place_in_queue=place_in_queue,
            canceled=False,
        )
        queue_member.save()
        log(log.INFO, "add_client_to_queue: QueueMember created [%d]", queue_member.id)

    def delete_client_from_queue(
        self, client_data: ClientQueue, doctor: Doctor
    ) -> None:
        client: ClientDB = ClientDB.query.filter(
            ClientDB.phone == client_data.phone
        ).first()

        if not client:
            log(
                log.ERROR,
                "delete_client_from_queue: Client [%s] is not registered",
                client_data.phone,
            )
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
            log(log.ERROR, "delete_client_from_queue: reception doesn't found")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Reception not found"
            )

        log(log.INFO, "delete_client_from_queue: reception today [%s]", reception.id)

        member_in_queue: QueueMember = QueueMember.query.filter(
            and_(
                QueueMember.reception_id == reception.id,
                QueueMember.client_id == client.id,
                QueueMember.canceled == False,  # noqa E712
            )
        ).first()

        if not member_in_queue:
            log(
                log.WARNING,
                "Not found query_member for client [%d], reception [%d]",
                client.id,
                reception.id,
            )
            return

        member_in_queue.canceled = True
        member_in_queue.save()

        log(
            log.INFO,
            "delete_client_from_queue: queue_member [%s] deleted",
            member_in_queue,
        )

    def identify_client_with_phone(
        self, phone_num: str, doctor: Doctor
    ) -> Union[Client, None]:
        doctor = DoctorDB.query.filter(DoctorDB.email == doctor.email).first()
        phone = "".join(re.findall(r"\d+", str(phone_num)))

        client = ClientDB.query.filter(ClientDB.phone == phone).first()
        if not client:
            log(
                log.ERROR,
                "identify_client_with_phone: No such phone number [%s]. Client is not registered",
                phone_num,
            )
            return
        self.add_client_to_queue(client, doctor)
        return client

    def get_client_with_phone(phone: str) -> Union[Client, None]:
        phone_number = "".join(re.findall(r"\d+", str(phone)))
        client = ClientDB.query.filter(ClientDB.phone == phone_number).first()
        if not client:
            log(
                log.ERROR,
                "get_client_with_phone: No such phone number [%s]. Client is not registered",
                phone,
            )
            return
        return client

    def get_queue(self, doctor: Doctor) -> List[ClientQueue]:
        today = datetime.date.today()
        reception = Reception.query.filter(Reception.date == today).first()
        if not reception:
            reception = Reception(doctor_id=doctor.id).save(True)

        log(
            log.INFO,
            "get_queue: reception [%s] today",
            reception,
        )

        queue_members = QueueMember.query.filter(
            and_(
                QueueMember.reception_id == reception.id,
                QueueMember.canceled == False,  # noqa E712
            )
        ).all()

        members = [
            {
                "client": member.client,
                "tests": [
                    {
                        "care_plan_id": test.care_plan_id
                        if test.care_plan_id
                        else None,
                        "client_id": test.client_id if test.client_id else None,
                        "date": test.date.strftime("%m/%d/%Y") if test.date else None,
                        "doctor_id": test.doctor_id if test.doctor_id else None,
                        "id": test.id if test.id else None,
                    }
                    for test in Test.query.filter(
                        Test.client_id == member.client.id
                    ).all()
                ],
                "canceled": member.canceled,
                "place_in_queue": member.place_in_queue,
            }
            for member in queue_members
        ]

        log(
            log.INFO,
            "get_queue: members count [%d] from queue",
            len(members),
        )

        members_in_queue = []
        for member in members:
            member_info = member["client"].client_info
            visit_info_with_end_date = []
            progress_date = None
            for visit in member_info["visits"]:
                if visit.end_time:
                    visit_info_with_end_date.append(visit)
                care_plans = CarePlan.query.filter(
                    CarePlan.client_id == visit.client_id
                ).all()
                for plan in care_plans:
                    if plan.end_time:
                        if plan.end_time.date() >= today:
                            progress_date = plan.progress_date
            client_member = {
                "api_key": member_info["api_key"],
                "email": member_info["email"],
                "first_name": member_info["firstName"],
                "id": member_info["id"],
                "last_name": member_info["lastName"],
                "phone": member_info["phone"],
                "req_date": member_info["req_date"].strftime("%m/%d/%Y, %H:%M:%S")
                if member_info["req_date"]
                else None,
                "place_in_queue": member["place_in_queue"],
                # TODO: rougue_mode
                # "rougue_mode": member_info,
                "progress_date": progress_date.strftime("%m/%d/%Y")
                if progress_date
                else None,
                "tests": member["tests"],
                "visits": visit_info_with_end_date,
            }
            visits = member_info["visits"]
            if not visits:
                members_in_queue.append(client_member)
            count_visits = len(visits)
            visit_with_end_time = []
            visit_without_end_time = []
            for visit in visits:
                if not visit.end_time:  # noqa E712
                    visit_without_end_time.append(visit)
                if visit.end_time:
                    visit_with_end_time.append(visit)
            if (
                count_visits > 0
                and count_visits == len(visit_with_end_time)
                and member["canceled"] == False  # noqa E712
            ):
                members_in_queue.append(client_member)
            elif len(visit_without_end_time) > 0:
                members_in_queue.append(client_member)

        log(
            log.INFO,
            "get_queue: members count [%d] without complete visit",
            len(members_in_queue),
        )

        return [member for member in members_in_queue]
