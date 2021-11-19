from typing import List
from fastapi import HTTPException, status

from app.schemas import Doctor, VisitInfoHistory, VisitHistory
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
        visits_history = [
            {"doctor_name": doctor.first_name, "date": visit.date.strftime("%m/%d/%Y")}
            for visit in visits
        ]

        return visits_history
