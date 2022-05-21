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
    CarePlan,
)
from app.logger import log


class NoteService:
    def write_note(self, data_note: NoteSchemas, doctor: Doctor) -> List[NoteSchemas]:
        client: ClientDB = ClientDB.query.filter(
            ClientDB.api_key == data_note.api_key
        ).first()
        if not client:
            log(log.ERROR, "write_note: Client not found")
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
            log(log.ERROR, "get_note: Client not found")
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

        care_plans = CarePlan.query.filter(CarePlan.client_id == client.id).all()

        log(log.INFO, "get_note: count [%d] of care plans", len(care_plans))

        time_today = datetime.datetime.utcnow().strftime("%m/%d/%Y, %H:%M:%S")

        care_plan = None
        if len(care_plans) > 0:
            for plan in care_plans:
                if not plan.end_time or plan.end_time >= datetime.datetime.strptime(
                    time_today, "%m/%d/%Y, %H:%M:%S"
                ):
                    log(log.INFO, "get_note: care plan end time [%s]", plan.end_time)
                    log(
                        log.INFO,
                        "get_note: time today [%s]",
                        datetime.datetime.strptime(time_today, "%m/%d/%Y, %H:%M:%S"),
                    )
                    care_plan = plan

        notes = Note.query.filter(Note.client_id == client.id).all()

        log(log.INFO, "get_note: count [%d] of notes", len(notes))

        get_notes = []

        if len(notes) > 0 and care_plan:
            care_plan_start_date = care_plan.start_time.date()
            for note in notes:
                if note.date >= care_plan_start_date:
                    get_notes.append(note)

        return get_notes

    def delete_note(self, data_note: NoteSchemas, doctor: Doctor) -> None:
        client: ClientDB = ClientDB.query.filter(
            ClientDB.api_key == data_note.api_key
        ).first()

        if not client:
            log(log.ERROR, "delete_note: Client not found")
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

        note: Note = Note.query.filter(Note.id == data_note.id).first()
        note.delete()

        log(log.INFO, "delete_note: note [%d] deleted", note.id)

        return
