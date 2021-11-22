import datetime

from fastapi import HTTPException, status
from app.schemas import Doctor, PostTest, CreateTest
from app.models import Client as ClientDB, Test
from app.logger import log


class TestService:
    def create_test(self, data: PostTest, doctor: Doctor) -> CreateTest:
        client: ClientDB = ClientDB.query.filter(
            ClientDB.api_key == data.api_key
        ).first()

        if not client:
            log(log.ERROR, "Client not found")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Client not found"
            )

        log(log.INFO, "Client [%s] for test", client)

        date = datetime.datetime.strptime(data.date, "%m/%d/%Y, %H:%M:%S")

        if not date:
            log(log.ERROR, "Date not found")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Front end Data don't send",
            )

        log(log.INFO, "Date [%s] for start test", date)

        create_test = Test(
            date=date,
            client_id=client.id,
            doctor_id=doctor.id,
        ).save()

        return create_test
