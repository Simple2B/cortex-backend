import datetime
from fastapi import HTTPException, status
from sqlalchemy.sql.elements import and_
from app.schemas import Client, ClientInfo, ClientInTake, Doctor, Note as NoteSchemas
from app.models import (
    Client as ClientDB,
    Condition,
    ClientCondition,
    Disease,
    ClientDisease,
    QueueMember as QueueMemberDB,
    Visit,
    Reception,
    Note,
)
from app.logger import log


class NoteService:
    def get_visit_for_note(self, api_key: str, doctor: Doctor) -> NoteSchemas:
        client: ClientDB = ClientDB.query.filter(ClientDB.api_key == api_key).first()
        if not client:
            log(log.ERROR, "get_visit_for_note: Client [%s] not found", client)
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Client not found"
            )

        log(log.INFO, "get_visit_for_note: Client [%s]", client)

        today = datetime.date.today()

        reception = Reception.query.filter(Reception.date == today).first()
        if not reception:
            reception = Reception(date=today, doctor_id=doctor.id).save()
            log(log.INFO, "get_visit_for_note: Today reception created [%s]", reception)

        log(log.INFO, "get_visit_for_note: Today reception [%s]", reception)

        visits = Visit.query.filter(
            and_(
                Visit.date == today,
                Visit.client_id == client.id,
                Visit.end_time == None,  # noqa E711
            )
        ).all()

        visits
