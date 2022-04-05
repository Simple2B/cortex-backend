import datetime
from typing import List

from fastapi import HTTPException, status
from sqlalchemy.sql.elements import and_

from app.schemas import Doctor, Consult as ConsultSchemas
from app.models import (
    Client as ClientDB,
    Visit,
    Reception,
    Consult,
)
from app.logger import log
from app.schemas.consult import ConsultDelete


class ConsultService:
    def write_consult(
        self, data_consult: ConsultSchemas, doctor: Doctor
    ) -> ConsultSchemas:
        client: ClientDB = ClientDB.query.filter(
            ClientDB.id == data_consult.client_id
        ).first()
        if not client:
            log(log.ERROR, "write_consult: Client not found")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Client not found"
            )

        log(log.INFO, "write_consult: Client [%s]", client)

        today = datetime.date.today()

        reception = Reception.query.filter(Reception.date == today).first()
        if not reception:
            reception = Reception(date=today, doctor_id=doctor.id).save()
            log(log.INFO, "write_consult: Today reception created [%s]", reception)

        log(log.INFO, "write_consult: Today reception [%s]", reception)

        visit: Visit = Visit.query.filter(
            and_(
                Visit.date == today,
                Visit.client_id == client.id,
                Visit.end_time == None,  # noqa E711
            )
        ).first()

        if not visit:
            log(log.INFO, "write_consult: client doesn't have visit")

            visit = Visit(
                date=today,
                client_id=client.id,
                doctor_id=doctor.id,
            )
            visit.save()

            log(
                log.INFO,
                "write_consult: visit [%d] created for client [%d]",
                visit.id,
                client.id,
            )

            consult = Consult(
                date=today,
                client_id=client.id,
                doctor_id=doctor.id,
                visit_id=visit.id,
                notes=data_consult.notes,
            ).save()

            log(
                log.INFO,
                "write_consult: note [%d] created for visit [%d]",
                consult.id,
                visit.id,
            )

        log(log.INFO, "write_consult: visit [%d] for note", visit.id)

        consult = Consult(
            date=today,
            client_id=client.id,
            doctor_id=doctor.id,
            visit_id=visit.id,
            consult=data_consult.consult,
        ).save()

        log(
            log.INFO,
            "write_consult: consult [%d] for today visit [%d] created ",
            consult.id,
            visit.id,
        )
        # consult.date.strftime("%m/%d/%Y")
        consult_write_to_visit = {
            "id": consult.id,
            "date": consult.date,
            "consult": consult.consult,
            "client_id": consult.client_id,
            "doctor_id": consult.doctor_id,
            "visit_id": consult.visit_id,
        }

        return consult_write_to_visit

    def get_consult(self, api_key: str, doctor: Doctor) -> List[ConsultSchemas]:
        client: ClientDB = ClientDB.query.filter(ClientDB.api_key == api_key).first()
        if not client:
            log(log.ERROR, "get_consult: Client not found")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Client not found"
            )

        log(log.INFO, "get_consult: Client [%s]", client)

        today = datetime.date.today()

        reception = Reception.query.filter(Reception.date == today).first()
        if not reception:
            reception = Reception(date=today, doctor_id=doctor.id).save()
            log(log.INFO, "get_consult: Today reception created [%s]", reception)

        log(log.INFO, "get_consult: Today reception [%s]", reception)

        visits: Visit = Visit.query.filter(
            and_(
                Visit.date == today,
                Visit.client_id == client.id,
                # Visit.end_time == None,  # noqa E711
            )
        ).all()
        today = today = datetime.datetime.utcnow()
        if len(visits) > 0:
            visit = visits[-1]

            log(
                log.INFO,
                "get_consult: visit [%s] for client [%d] today",
                visit,
                client.id,
            )

            consults_client = Consult.query.filter(Consult.client_id == client.id).all()

            consults = []
            for consult in consults_client:
                if consult.visit.end_time and consult.visit.end_time >= today:
                    consults.append(consult)
            return consults_client

        log(log.INFO, "get_consult: client doesn't have visit")
        visit: Visit = Visit(
            date=today,
            client_id=client.id,
            doctor_id=doctor.id,
        )
        visit.save()
        log(
            log.INFO,
            "get_consult: visit [%s] for client [%d] today created",
            visit,
            client.id,
        )
        return []

    def delete_consult(self, data_consult: ConsultDelete, doctor: Doctor) -> None:

        client: ClientDB = ClientDB.query.filter(
            ClientDB.id == data_consult.client_id
        ).first()
        if not client:
            log(log.ERROR, "delete_consult: Client not found")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Client not found"
            )

        log(log.INFO, "delete_consult: Client [%s]", client)

        today = datetime.date.today()

        reception = Reception.query.filter(Reception.date == today).first()
        if not reception:
            reception = Reception(date=today, doctor_id=doctor.id).save()
            log(log.INFO, "delete_consult: Today reception created [%s]", reception)

        log(log.INFO, "delete_consult: Today reception [%s]", reception)

        consult: Consult = Consult.query.filter(Consult.id == data_consult.id).first()
        consult.delete()

        log(log.INFO, "delete_consult: consult [%d] deleted", consult.id)

        return
