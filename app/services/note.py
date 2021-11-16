import datetime
from typing import List
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
    def write_note(self, data_note: NoteSchemas, doctor: Doctor) -> List[NoteSchemas]:
        client: ClientDB = ClientDB.query.filter(
            ClientDB.id == data_note.client_id
        ).first()
        if not client:
            log(log.ERROR, "write_note: Client [%s] not found", client)
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Client not found"
            )

        log(log.INFO, "write_note: Client [%s]", client)

        today = datetime.date.today()

        reception = Reception.query.filter(Reception.date == today).first()
        if not reception:
            reception = Reception(date=today, doctor_id=doctor.id).save()
            log(log.INFO, "write_note: Today reception created [%s]", reception)

        log(log.INFO, "write_note: Today reception [%s]", reception)

        visit: Visit = Visit.query.filter(
            and_(
                Visit.date == today,
                Visit.client_id == client.id,
                Visit.end_time == None,  # noqa E711
            )
        ).first()

        if not visit:
            log(log.INFO, "write_note: client doesn't have visit")

            visit = Visit(
                date=today,
                client_id=client.id,
                doctor_id=doctor.id,
            )
            visit.save()

            log(
                log.INFO,
                "write_note: visit [%d] created for client [%d]",
                visit.id,
                client.id,
            )

            note = Note(
                date=today,
                client_id=client.id,
                doctor_id=doctor.id,
                visit_id=visit.id,
                notes=data_note.notes,
            ).save()

            log(
                log.INFO,
                "write_note: note [%d] created for visit [%d]",
                note.id,
                visit.id,
            )

        log(log.INFO, "write_note: visit [%d] for note", visit.id)

        note = Note(
            date=today,
            client_id=client.id,
            doctor_id=doctor.id,
            visit_id=visit.id,
            notes=data_note.notes,
        ).save()

        log(
            log.INFO,
            "write_note: note [%d] for today visit [%d] created ",
            note.id,
            visit.id,
        )

        return visit.visit_info

    def get_note(self, api_key: str, doctor: Doctor) -> List[NoteSchemas]:
        client: ClientDB = ClientDB.query.filter(ClientDB.api_key == api_key).first()
        if not client:
            log(log.ERROR, "get_note: Client [%s] not found", client)
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Client not found"
            )

        log(log.INFO, "get_note: Client [%s]", client)

        today = datetime.date.today()

        reception = Reception.query.filter(Reception.date == today).first()
        if not reception:
            reception = Reception(date=today, doctor_id=doctor.id).save()
            log(log.INFO, "get_note: Today reception created [%s]", reception)

        log(log.INFO, "get_note: Today reception [%s]", reception)

        visit: Visit = Visit.query.filter(
            and_(
                Visit.date == today,
                Visit.client_id == client.id,
                Visit.end_time == None,  # noqa E711
            )
        ).first()

        if not visit:
            log(log.INFO, "get_note: client doesn't have visit")

        log(log.INFO, "get_note: visit [%s] for client [%d] today", visit, client.id)

        notes = visit.visit_info["notes"]

        return notes

    def delete_note(self, data_note: NoteSchemas, doctor: Doctor) -> None:

        client: ClientDB = ClientDB.query.filter(
            ClientDB.id == data_note.client_id
        ).first()
        if not client:
            log(log.ERROR, "delete_note: Client [%s] not found", client)
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Client not found"
            )

        log(log.INFO, "delete_note: Client [%s]", client)

        today = datetime.date.today()

        reception = Reception.query.filter(Reception.date == today).first()
        if not reception:
            reception = Reception(date=today, doctor_id=doctor.id).save()
            log(log.INFO, "delete_note: Today reception created [%s]", reception)

        log(log.INFO, "delete_note: Today reception [%s]", reception)

        visit: Visit = Visit.query.filter(
            and_(
                Visit.date == today,
                Visit.client_id == client.id,
                Visit.end_time == None,  # noqa E711
            )
        ).first()

        if not visit:
            log(log.INFO, "delete_note : client doesn't have visit")

        log(log.INFO, "delete_note: visit [%s] for client [%d] today", visit, client.id)

        note: Note = Note.query.filter(
            and_(Note.id == data_note.id, Note.visit_id == visit.id)
        ).first()
        note.delete()

        log(log.INFO, "delete_note: note [%d] deleted", note.id)

        return
