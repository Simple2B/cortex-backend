import datetime
from fastapi import HTTPException, status
from sqlalchemy.sql.elements import and_
from app.schemas import Client, ClientInfo, ClientInTake, Doctor
from app.models import (
    Client as ClientDB,
    Condition,
    ClientCondition,
    Disease,
    ClientDisease,
    QueueMember as QueueMemberDB,
    Visit,
)
from app.logger import log


class ClientService:
    @staticmethod
    def link_client_condition(client_id: int, condition_name: str):
        condition = Condition.query.filter(Condition.name == condition_name).first()
        if not condition:
            condition = Condition(name=condition_name).save()
            log(log.INFO, "Condition [%s] has been saved", condition.name)
        ClientCondition(client_id=client_id, condition_id=condition.id).save()

    @staticmethod
    def link_client_disease(client_id: int, disease_name: str):
        disease = Disease.query.filter(Disease.name == disease_name).first()
        if not disease:
            disease = Disease(name=disease_name).save()
            log(log.INFO, "Disease [%s] has been saved", disease.name)
        ClientDisease(client_id=client_id, disease_id=disease.id).save()

    @staticmethod
    def register(client_data: ClientInfo) -> ClientDB:
        client = ClientDB(
            first_name=client_data.firstName,
            last_name=client_data.lastName,
            birthday=datetime.datetime.strptime(client_data.birthday, "%Y-%m-%d").date()
            if client_data.birthday
            else None,
            address=client_data.address,
            city=client_data.city,
            state=client_data.state,
            zip=client_data.zip,
            phone=client_data.phone,
            email=client_data.email,
            referring=client_data.referring,
            medications=client_data.medications,
            covid_tested_positive=client_data.covidTestedPositive.value,
            covid_vaccine=client_data.covidVaccine.value,
            stressful_level=client_data.stressfulLevel,
            consent_minor_child=client_data.consentMinorChild,
            relationship_child=client_data.relationshipChild,
        ).save()
        log(log.INFO, "Client [%s] has been registered", client.first_name)

        for condition_name in client_data.conditions:
            ClientService.link_client_condition(client.id, condition_name)

        if client_data.otherCondition:
            ClientService.link_client_condition(client.id, client_data.otherCondition)

        for disease_name in client_data.diseases:
            ClientService.link_client_disease(client.id, disease_name)

        return client

    def register_new_client(self, client_data: ClientInfo) -> Client:
        log(log.INFO, "Register_new_client: client_data [%s] ", client_data)

        client = ClientDB.query.filter(ClientDB.phone == client_data.phone).first()
        if not client:
            log(log.INFO, "Client [%s] must registered", client_data.firstName)
            client_with_email = ClientDB.query.filter(
                ClientDB.email == client_data.email
            ).first()
            if client_with_email:
                ClientCondition.query.filter(
                    ClientCondition.client_id == client_with_email.id
                ).delete()
                ClientDisease.query.filter(
                    ClientDisease.client_id == client_with_email.id
                ).delete()
                Visit.query.filter(Visit.client_id == client_with_email.id).delete()
                QueueMemberDB.query.filter(
                    QueueMemberDB.client_id == client_with_email.id
                ).delete()

                log(log.INFO, "Such email [%s] exists", client_with_email)
                client_with_email.delete()

                log(log.INFO, "Email [%s] deleted", client_with_email)

            client = self.register(client_data)
            log(log.INFO, "Added client [%s]", client)
        else:
            client.first_name = client_data.firstName
            client.last_name = client_data.lastName
            client.birthday = client_data.birthday
            client.birthday = (
                datetime.datetime.strptime(client_data.birthday, "%Y-%m-%d").date()
                if client_data.birthday
                else None
            )
            client.address = client_data.address
            client.city = client_data.city
            client.state = client_data.state
            client.zip = client_data.zip
            client.phone = client_data.phone
            client.email = client_data.email
            client.referring = client_data.referring
            client.medications = client_data.medications
            client.covid_tested_positive = client_data.covidTestedPositive.value
            client.covid_vaccine = client_data.covidVaccine.value
            client.stressful_level = client_data.stressfulLevel
            client.consent_minor_child = client_data.consentMinorChild
            client.relationship_child = client_data.relationshipChild

            log(log.INFO, "Client [%d] updated [%s]", client.id, client.first_name)

            ClientCondition.query.filter(
                ClientCondition.client_id == client.id
            ).delete()
            for condition_name in client_data.conditions:
                ClientService.link_client_condition(client.id, condition_name)

            if client_data.otherCondition:
                ClientService.link_client_condition(
                    client.id, client_data.otherCondition
                )

            ClientDisease.query.filter(ClientDisease.client_id == client.id).delete()
            for disease_name in client_data.diseases:
                ClientService.link_client_disease(client.id, disease_name)

            return client.save()

        return client

    @staticmethod
    def intake(client_data: ClientInTake, doctor: Doctor) -> ClientInfo:
        client: ClientDB = ClientDB.query.filter(
            ClientDB.api_key == client_data.api_key
        ).first()
        if not client:
            log(log.ERROR, "Client [%s] not found", client)
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Client not found"
            )

        log(log.INFO, "Client [%s] for intake", client)

        visit = Visit(
            date=datetime.date.today(),
            # TODO -> end_time
            start_time=datetime.datetime.now(),
            # end_time=datetime.datetime.now() + datetime.timedelta(minutes=30),
            rougue_mode=client_data.rougue_mode,
            client_id=client.id,
            doctor_id=doctor.id,
        ).save()

        log(log.INFO, "Client Intake: Visit created [%d]", visit.id)
        client_in_queue: QueueMemberDB = QueueMemberDB.query.filter(
            QueueMemberDB.client_id == client.id
        ).first()

        if not client_in_queue:
            raise HTTPException(
                status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
                detail="Client doesn't at queue",
            )

        if client_in_queue:
            client_in_queue.visit_id = visit.id
            client_in_queue.save()
            log(
                log.INFO, "Client in queue [%s] goto visit [%s]", client_in_queue, visit
            )
        log(log.INFO, "POST: Client_info in queue [%s]", client.client_info)
        return client.client_info

    @staticmethod
    def get_intake(api_key: str, doctor: Doctor) -> ClientInfo:

        client: ClientDB = ClientDB.query.filter(ClientDB.api_key == api_key).first()

        if not client:
            log(log.ERROR, "No such client with api_key [%s]", api_key)
            raise HTTPException(
                status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
                detail="No such client with api_key",
            )

        today = datetime.date.today()

        visit: Visit = Visit.query.filter(
            and_(
                Visit.date == today,
                Visit.doctor_id == doctor.id,
                Visit.client_id == client.id,
            )
        ).first()

        log(log.INFO, "GET: get_intake client with visit [%s]", visit)

        if not visit:
            log(log.ERROR, "No reception today")
            raise HTTPException(
                status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
                detail="No reception today",
            )

        return client.client_info
