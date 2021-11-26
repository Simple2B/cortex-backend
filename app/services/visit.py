import datetime
from typing import List
from fastapi import HTTPException, status

from app.schemas import Doctor, VisitInfoHistory, VisitHistory, VisitHistoryFilter
from app.models import Client as ClientDB
from app.logger import log


class VisitService:
    def get_history_visit(self, api_key: str, doctor: Doctor) -> List[VisitHistory]:
        client: ClientDB = ClientDB.query.filter(ClientDB.api_key == api_key).first()
        if not client:
            log(log.ERROR, "get_history_visit: Client not found")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Client not found"
            )

        log(log.INFO, "get_history_visit: Client [%s]", client)
        visits: VisitInfoHistory = client.client_info["visits"]

        log(log.INFO, "get_history_visit: Count [%d] of visits ", len(visits))
        visits_history = []
        for visit in visits:
            if visit.end_time:
                visits_history.append(
                    {
                        "doctor_name": doctor.first_name,
                        "date": visit.date.strftime("%m/%d/%Y"),
                    }
                )

        return visits_history

    def filter_visits(
        self, data: VisitHistoryFilter, doctor: Doctor
    ) -> List[VisitHistory]:
        client: ClientDB = ClientDB.query.filter(
            ClientDB.api_key == data.api_key
        ).first()
        if not client:
            log(log.ERROR, "filter_visits: Client not found")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Client not found"
            )

        log(log.INFO, "filter_visits: Client [%s]", client)

        visits = client.client_info["visits"]
        log(
            log.INFO,
            "filter_visits: Count of all visits [%d] for client [%s]",
            len(visits),
            client,
        )

        visits_report = []

        for visit in visits:
            if visit.end_time:
                log(
                    log.INFO,
                    "filter_visits: visit [%s] with end_time]",
                    visit,
                )
                visit_start_time = datetime.datetime.strptime(
                    visit.start_time.strftime("%m/%d/%Y, %H:%M:%S"),
                    "%m/%d/%Y, %H:%M:%S",
                )
                log(
                    log.INFO,
                    "filter_visits: visit start_time [%s]",
                    visit_start_time,
                )
                visit_end_time = datetime.datetime.strptime(
                    visit.end_time.strftime("%m/%d/%Y, %H:%M:%S"),
                    "%m/%d/%Y, %H:%M:%S",
                )
                log(
                    log.INFO,
                    "filter_visits: visit end_time [%s]",
                    visit_end_time,
                )
                if visit_start_time >= datetime.datetime.strptime(
                    data.start_time, "%m/%d/%Y, %H:%M:%S"
                ) and visit_end_time <= datetime.datetime.strptime(
                    data.end_time, "%m/%d/%Y, %H:%M:%S"
                ):
                    visits_report.append(visit)

        if len(visits_report) > 0:

            filter_visits = [
                {
                    "doctor_name": doctor.first_name,
                    "date": visit.date.strftime("%m/%d/%Y"),
                }
                for visit in visits_report
            ]
            log(log.INFO, "filter_visits: Count of visits [%d]", len(filter_visits))

            return filter_visits
        return []
