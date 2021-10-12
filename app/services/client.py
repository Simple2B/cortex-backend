import datetime
from app.schemas import Client, ClientInfo, ClientPhone
from app.models import (
    Client as ClientDB,
    Condition,
    ClientCondition,
    Disease,
    ClientDisease,
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
        client = ClientDB.query.filter(ClientDB.phone == client_data.phone).first()
        if not client:
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

    def identify_client_with_phone(self, phone_num: ClientPhone) -> Client:
        client = ClientDB.query.filter(ClientDB.phone == phone_num.phone).first()
        return client
