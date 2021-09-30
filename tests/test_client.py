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

    client_data = {
        "firstName": "Alex",
        "lastName": "Brown",
        "dateBirth": "2021-09-16",
        "address": "Street",
        "city": "New York",
        "state": "US",
        "zip": "02232",
        "phone": "19077653340",
        "email": "client@gmail.com",
        "checkBoxesСonditions": {
            "conditions": {
                "1": "Dizziness",
                "2": "Asthma",
                "3": "Obesity",
            },
            "otherLabel": "",
        },
        "checkboxesFollowing": {
            "1": "Concussion",
            "2": "Diabetes",
        },
        "medications": "",
        "testedPositive": "Rather not say",
        "covidVaccine": "",
        "stressfulLevel": "5",
        "consentMinorChild": "",
        "relationshipChild": "",
    }
    # 1. add Client into DB (client_data)
    response = client.post("/client/registration", client_data=client_data)
    assert response
    assert response.ok
