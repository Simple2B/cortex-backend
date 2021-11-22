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
    Reception,
)
from app.logger import log


class ClientService:
    @staticmethod
    def link_client_condition(client_id: int, condition_name: str):
        condition = Condition.query.filter(Condition.name == condition_name).first()
        if not condition:
            condition = Condition(name=condition_name).save(True)
            log(log.INFO, "Condition [%s] has been saved", condition.name)
        ClientCondition(client_id=client_id, condition_id=condition.id).save(True)

    @staticmethod
    def link_client_disease(client_id: int, disease_name: str):
        disease = Disease.query.filter(Disease.name == disease_name).first()
        if not disease:
            disease = Disease(name=disease_name).save(True)
            log(log.INFO, "Disease [%s] has been saved", disease.name)
        ClientDisease(client_id=client_id, disease_id=disease.id).save(True)

    @staticmethod
    def register(client_data: ClientInfo) -> ClientDB:
        covidTestedPositive = client_data.covidTestedPositive
        covidVaccine = client_data.covidVaccine
        covidTestedPositive = (
            client_data.covidTestedPositive.value if covidTestedPositive else "null"
        )
        covidVaccine = client_data.covidVaccine.value if covidVaccine else "null"
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
            covid_tested_positive=covidTestedPositive,
            covid_vaccine=covidVaccine,
            stressful_level=client_data.stressfulLevel,
            consent_minor_child=client_data.consentMinorChild,
            relationship_child=client_data.relationshipChild,
        ).save(True)
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
            client.covid_tested_positive = (
                "null"
                if not client_data.covidTestedPositive
                else client_data.covidTestedPositive.value
            )
            client.covid_vaccine = (
                "null"
                if not client_data.covidVaccine
                else client_data.covidVaccine.value
            )
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

            return client.save(True)

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

        today = datetime.date.today()

        reception = Reception.query.filter(Reception.date == today).first()
        if not reception:
            reception = Reception(date=today, doctor_id=doctor.id).save()
            log(log.INFO, "Client Intake: Today reception created [%s]", reception)

        log(log.INFO, "Client Intake: Today reception [%s]", reception)

        client_in_queue: QueueMemberDB = QueueMemberDB.query.filter(
            and_(
                QueueMemberDB.client_id == client.id,
                QueueMemberDB.reception_id == reception.id,
                QueueMemberDB.canceled == False,  # noqa E712
            )
        ).first()

        log(
            log.INFO,
            "Client Intake: client in queue for today reception [%s]",
            client_in_queue,
        )

        visits = Visit.query.filter(
            and_(
                Visit.date == today,
                Visit.client_id == client.id,
                Visit.end_time == None,  # noqa E711
            )
        ).all()

        all_visits = Visit.query.filter(
            and_(
                Visit.date == today,
                Visit.client_id == client.id,
            )
        ).all()

        if not visits:
            visit = Visit(
                date=today,
                start_time=datetime.datetime.now(),
                # TODO: rougue_mode
                rougue_mode=client_data.rougue_mode,
                client_id=client.id,
                doctor_id=doctor.id,
            ).save()
            log(
                log.INFO,
                "Client Intake: visit [%d] for today created [%d]",
                len(all_visits) + 1,
                visit.id,
            )

            client_in_queue.visit_id = visit.id
            client_in_queue.save()

        log(
            log.INFO,
            "Client Intake: client visits [%s]",
            visits,
        )

        for visit in visits:
            if not visit.end_time:
                visit.start_time = datetime.datetime.now()
                # TODO: visit.rougue_mode
                visit.doctor_id = doctor.id
                visit.save()

                client_in_queue.visit_id = visit.id
                client_in_queue.save()

                log(
                    log.INFO,
                    "Client in queue [%s] go to visit again [%s]",
                    client_in_queue.client,
                    visit.id,
                )

        return client.client_info

    def complete_client_visit(self, client_data: ClientInTake, doctor: Doctor) -> None:
        log(log.INFO, "complete_client_visit: complete client_data [%s]", client_data)
        client: ClientDB = ClientDB.query.filter(
            ClientDB.api_key == client_data.api_key
        ).first()

        if not client:
            log(log.ERROR, "complete_client_visit: Client doesn't registration")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Client not found"
            )

        log(
            log.INFO,
            "complete_client_visit: Client [%d] [%s] from db",
            client.id,
            client.first_name,
        )

        today = datetime.date.today()

        reception = Reception.query.filter(Reception.date == today).first()

        if not reception:
            log(log.INFO, "complete_client_visit: reception didn't created")
            reception = Reception(date=today, doctor_id=doctor.id).save()
            log(log.INFO, "Client Intake: Today reception created [%s]", reception)

        visit: Visit = Visit.query.filter(
            and_(
                Visit.client_id == client.id,
                Visit.end_time == None,  # noqa E711
                Visit.doctor_id == doctor.id,
                Visit.date == today,
            )
        ).first()

        if not visit:
            log(log.ERROR, "complete_client_visit: Visit doesn't created")
            # raise HTTPException(
            #     status_code=status.HTTP_404_NOT_FOUND, detail="Visit doesn't created!"
            # )
            # return
            visit = Visit(
                end_time=datetime.datetime.utcnow(),
                client_id=client.id,
                doctor_id=doctor.id,
            ).save()

            QueueMemberDB(
                canceled=True,
                client_id=client.id,
                visit_id=visit.id,
                reception_id=reception.id,
            ).save()
            log(
                log.ERROR,
                "complete_client_visit: Visit created and complete [%d]",
                visit.id,
            )
            return
        visit.end_time = datetime.datetime.utcnow()
        visit.save()

        log(
            log.INFO,
            "complete_client_visit: Visit [%d] found for client [%s] for today [%s]",
            visit.id,
            client.first_name,
            today,
        )

        queue_members: QueueMemberDB = QueueMemberDB.query.filter(
            and_(
                QueueMemberDB.reception_id == reception.id,
                QueueMemberDB.canceled == False,  # noqa E712
                QueueMemberDB.visit_id == visit.id,
            )
        ).first()

        queue_members.visit_id

        queue_members.canceled = True
        queue_members.save()

        log(
            log.INFO,
            "complete_client_visit: Visit [%d] close for client [%s] for today [%s]",
            visit.id,
            client.first_name,
            today,
        )

    @staticmethod
    def get_intake(api_key: str, doctor: Doctor) -> ClientInfo:

        client: ClientDB = ClientDB.query.filter(ClientDB.api_key == api_key).first()

        if not client:
            log(log.ERROR, "get_intake: No such client with api_key [%s]", api_key)
            raise HTTPException(
                status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
                detail="get_intake: No such client with api_key",
            )

        today = datetime.date.today()

        reception = Reception.query.filter(Reception.date == today).first()

        if not reception:
            log(log.INFO, "get_intake: reception didn't created")
            reception = Reception(date=today, doctor_id=doctor.id).save()
            log(log.INFO, "get_intake: Today reception created [%s]", reception)

        log(log.INFO, "get_intake: reception created [%s]", reception)

        visit: Visit = Visit.query.filter(
            and_(
                Visit.date == today,
                Visit.doctor_id == doctor.id,
                Visit.client_id == client.id,
            )
        ).first()

        log(log.INFO, "GET: get_intake client with visit [%s]", visit)

        if not visit:
            log(log.INFO, "get_intake: No client visit, client from db")
            visit = Visit(
                date=today,
                client_id=client.id,
                doctor_id=doctor.id,
            )
            visit.save()
            log(log.INFO, "get_intake: Created visit [%d]", visit.id)
            return client.client_info

        return client.client_info
