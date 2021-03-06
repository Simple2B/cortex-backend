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
            ClientDB.id == data_note.client_id
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

        if not data_note.visit_id:
            start_time = datetime.datetime.strptime(
                data_note.start_time, "%m/%d/%Y, %H:%M:%S"
            )
            end_time = datetime.datetime.strptime(
                data_note.end_time, "%m/%d/%Y, %H:%M:%S"
            )
            visit = Visit(
                date=start_time,
                start_time=start_time,
                end_time=end_time,
                client_id=client.id,
                doctor_id=doctor.id,
            )
            visit.save()

            log(log.INFO, "write_note: save visit [%d] for update care plan", visit.id)

            note = Note(
                date=today,
                client_id=client.id,
                doctor_id=doctor.id,
                visit_id=visit.id,
                notes=data_note.notes,
            ).save()

            log(
                log.INFO,
                "write_note: note [%d] of visit [%d] created for care plan updated",
                note.id,
                visit.id,
            )

            return visit.visit_info

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

        visits: Visit = Visit.query.filter(Visit.client_id == client.id).all()
        visits_with_end_time = []
        if len(visits) > 0:
            for visit in visits:
                if visit.end_time:
                    visits_with_end_time.append(visit)
            visits_with_end_time.append(visits[-1])
        today = today = datetime.datetime.utcnow()
        log(
            log.INFO,
            "get_note: Count of visits with end time [%d]",
            len(visits_with_end_time),
        )
        care_plans = CarePlan.query.filter(CarePlan.client_id == client.id).all()

        if len(visits_with_end_time) > 0:
            log(
                log.INFO,
                "get_note: visit count [%d] for client [%d] today",
                len(visits_with_end_time),
                client.id,
            )
            care_plan = None
            if len(care_plans) > 0:
                for plan in care_plans:
                    if not plan.end_time or plan.end_time >= today:
                        care_plan = plan

            for visit in visits_with_end_time:
                notes = []
                # if visit.end_time is None or visit.end_time >= today:
                if care_plan:
                    #     log(log.INFO, "get_note: care plan [%s]", care_plan)
                    if (
                        not care_plan.end_time
                        and care_plan.start_time <= visit.start_time
                        or care_plan.start_time <= visit.start_time
                        and care_plan.end_time >= visit.end_time
                    ):
                        notes = [note for note in visit.visit_info["notes"]]
                        return notes
                    # notes = [
                    #     note
                    #     for note in visit.visit_info["notes"]
                    #     if note.date >= care_plan.start_time.date()
                    # ]
                    # return notes
                notes = [note for note in visit.visit_info["notes"]]
                return notes

        log(log.INFO, "get_note: client doesn't have visit")
        visit = Visit(
            date=today,
            client_id=client.id,
            doctor_id=doctor.id,
        ).save()
        log(
            log.INFO,
            "get_note: visit [%s] for client [%d] today created",
            visit,
            client.id,
        )
        return []

    def delete_note(self, data_note: NoteSchemas, doctor: Doctor) -> None:

        client: ClientDB = ClientDB.query.filter(
            ClientDB.id == data_note.client_id
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
