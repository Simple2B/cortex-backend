import pytest
from typing import Generator
from fastapi.testclient import TestClient

import tests.setup  # noqa: F401
from app.database import engine, Base

from app.setup import create_app
from app.models import (
    Client,
    ClientCondition,
    ClientDisease,
    Condition,
    Disease,
    Doctor,
    Visit,
    QueueMember,
)
from .database import generate_test_data


@pytest.fixture()
def client() -> Generator:
    app = create_app()
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    with TestClient(app) as c:
        yield c
    Base.metadata.drop_all(bind=engine)
    engine.dispose()


def test_client(client: TestClient):

    TEST_CONDITIONS = ["Dizziness", "Asthma", "Obesity"]
    TEST_DISEASES = ["Concussion", "Diabetes"]

    data = {
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

    # 1. add Client into DB (client_data)
    response = client.post("/api/client/registration", json=data)
    assert response
    assert response.ok

    client = Client.query.first()
    assert client
    condition_names_in_db = [c.name for c in Condition.query.all()]
    for condition_name in TEST_CONDITIONS:
        assert condition_name in condition_names_in_db

    disease_names_in_db = [d.name for d in Disease.query.all()]
    for disease_name in TEST_DISEASES:
        assert disease_name in disease_names_in_db

    conditions = ClientCondition.query.filter(
        ClientCondition.client_id == client.id
    ).all()
    assert len(conditions) == 4
    desesses = ClientDisease.query.filter(ClientDisease.client_id == client.id).all()
    assert len(desesses) == 2


def test_generate_data(client: TestClient):
    generate_test_data()

    assert len(Client.query.all()) == 10
    assert len(Doctor.query.all()) == 1
    assert len(Visit.query.all()) > 0
    assert len(QueueMember.query.all()) > 0
