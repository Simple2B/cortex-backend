import pytest
from typing import Generator
from fastapi.testclient import TestClient

import tests.setup  # noqa: F401
from app.database import engine, Base

from app.setup import create_app
from app.models import Client, ClientCondition, ClientDisease, Condition, Disease

from .database import generate_test_data


@pytest.fixture()
def client() -> Generator:
    app = create_app()
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    with TestClient(app) as c:
        generate_test_data()
        yield c
    Base.metadata.drop_all(bind=engine)
    engine.dispose()


TEST_CONDITIONS = ["Dizziness", "Asthma", "Obesity"]
TEST_DISEASES = ["Concussion", "Diabetes"]

data = {
    "id": 11,
    "firstName": "Alex",
    "lastName": "Brown",
    "birthday": "2000-09-16",
    "address": "Street",
    "city": "New York",
    "state": "US",
    "zip": "02232",
    "phone": "19077653340",
    "email": "client@gmail.com",
    "referring": "referring",
    "conditions": TEST_CONDITIONS,
    "otherCondition": "hvoroba",
    "diseases": TEST_DISEASES,
    "medications": "aspirin",
    "covidTestedPositive": True,
    "covidVaccine": False,
    "stressfulLevel": 5,
    "consentMinorChild": False,
    "relationshipChild": "",
}


def test_client(client: TestClient):
    # 1. add Client into DB (client_data)
    response = client.post("/api/client/registration", json=data)
    assert response
    assert response.ok

    client_db = Client.query.filter(Client.email == data["email"]).first()
    assert client_db
    condition_names_in_db = [c.name for c in Condition.query.all()]
    for condition_name in TEST_CONDITIONS:
        assert condition_name in condition_names_in_db

    disease_names_in_db = [d.name for d in Disease.query.all()]
    for disease_name in TEST_DISEASES:
        assert disease_name in disease_names_in_db

    conditions = ClientCondition.query.filter(
        ClientCondition.client_id == client_db.id
    ).all()
    assert len(conditions) == 4
    desesses = ClientDisease.query.filter(ClientDisease.client_id == client_db.id).all()
    assert len(desesses) == 2

    # 1. get Clients
    response = client.get("/api/client/clients")
    assert response
    assert response.ok


def test_get_queue(client: TestClient):
    data_client = {
        "id": 11,
        # "api_key": Optional[str]
        "first_name": "Alex",
        "last_name": "Brown",
        "phone": "19077653340",
        "email": "client@gmail.com",
    }
    # add client for queue
    response = client.post("/api/client/add_clients_queue", json=data_client)
    assert response
    assert response.ok


def test_get_queue(client: TestClient):
    # 1. get Queue
    response = client.get("/api/client/queue")
    assert response
    assert response.ok
