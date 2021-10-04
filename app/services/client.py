from app.schemas import Client, ClientInfo
from app.models import Client as ClientDB, Condition, ClientCondition, Disease, ClientDisease
from app.logger import log


class ClientService:
    @staticmethod
    def link_client_condition(client_id: int, condition_name: str):
        condition = Condition.query.filter(Condition.name == condition_name).first()
        if not condition:
            condition = Condition(name=condition_name).save()
        ClientCondition(client_id=client_id, condition_id=condition.id).save()

    @staticmethod
    def link_client_disease(client_id: int, disease_name: str):
        disease = Disease.query.filter(Disease.name == disease_name).first()
        if not disease:
            disease = Disease(name=disease_name).save()
        ClientDisease(client_id=client_id, disease_id=disease.id).save()

    @staticmethod
    def register(client_data: ClientInfo) -> ClientDB:
        client = ClientDB(
            first_name=client_data.firstName,
            last_name=client_data.lastName,
            birthday=client_data.birthday,
            address=client_data.address,
            city=client_data.city,
            state=client_data.state,
            zip=client_data.zip,
            phone=client_data.phone,
            email=client_data.email,
            medications=client_data.medications,
            covid_tested_positive=client_data.covidTestedPositive,
            covid_vaccine=client_data.covidVaccine,
            stressful_level=client_data.stressfulLevel,
            consent_minor_child=client_data.consentMinorChild,
            relationship_child=client_data.relationshipChild,
        ).save()

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
            client.first_name = client_data.first_name
            client.last_name = client_data.last_name
            client.birthday = client_data.birthday,
            client.address = client_data.address,
            client.city = client_data.city,
            client.state = client_data.state,
            client.zip = client_data.zip,
            client.phone = client_data.phone,
            client.email = client_data.email,
            client.medications = client_data.medications,
            client.covid_tested_positive = client_data.covid_tested_positive,
            client.covid_vaccine = client_data.covid_vaccine,
            client.stressful_level = client_data.stressful_level,
            client.consent_minor_child = client_data.consent_minor_child,
            client.relationship_child = client_data.relationship_child,

            ClientCondition.query.filter(ClientCondition.client_id == client.id).delete()
            for condition_name in client_data.conditions:
                ClientService.link_client_condition(client.id, condition_name)

            if client_data.other_condition:
                ClientService.link_client_condition(client.id, client_data.other_condition)

            ClientDisease.query.filter(ClientDisease.client_id == client.id).delete()
            for disease_name in client_data.diseases:
                ClientService.link_client_disease(client.id, disease_name)

            return client.save()

        return client
