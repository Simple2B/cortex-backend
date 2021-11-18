import datetime
from typing import List
from fastapi import HTTPException, status
from sqlalchemy.sql.elements import and_
from app.schemas import Doctor, VisitHistory
from app.models import Client as ClientDB
from app.logger import log


class VisitService:
    def get_history_visit(self, api_key: str, doctor: Doctor) -> List[VisitHistory]:
        client: ClientDB = ClientDB.query.filter(ClientDB.api_key == api_key).first()
        visits = client.client_info["visits"]
        return visits
