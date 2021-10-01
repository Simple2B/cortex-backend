import pytest
from typing import Generator
from fastapi.testclient import TestClient

import tests.setup  # noqa: F401
from app.database import engine, Base

from app.setup import create_app


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
        "conditions": ["Dizziness", "Asthma", "Obesity"],
        "otherCondition": "hvoroba",
        "diseases": ["Concussion", "Diabetes"],
        "medications": "aspirin",
        "covidTestedPositive": True,
        "covidVaccine": False,
        "stressfulLevel": 5,
        "consentMinorChild": False,
        "relationshipChild": "",
    }

    # 1. add Client into DB (client_data)
    response = client.post("/client/registration", client_data=data)
    assert response
    assert response.ok
