import datetime
from fastapi import HTTPException, status
from sqlalchemy.sql.elements import and_
from app.schemas import Doctor, Note as NoteSchemas
from app.models import (
    Client as ClientDB,
    Visit,
    Reception,
    Note,
)
from app.logger import log


class NoteService:
    def write_note(self, data_note: NoteSchemas, doctor: Doctor) -> None:
        client: ClientDB = ClientDB.query.filter(
            ClientDB.id == data_note.client_id
        ).first()
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

        visit = Visit.query.filter(
            and_(
                Visit.date == today,
                Visit.client_id == client.id,
                Visit.end_time == None,  # noqa E711
            )
        ).first()

        note: Note = Note.query.filter(Note.visit_id == visit.id).first()
        note.notes = data_note.notes
        note.save()
