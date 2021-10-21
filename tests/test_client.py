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
    Visit,
    Doctor,
    Reception,
    QueueMember,
)

from .database import generate_test_data, CLIENT_NUMBER
from .utils import login


@pytest.fixture()
def client() -> Generator:
    app = create_app()
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    with TestClient(app) as c:
        generate_test_data()
        token = login(c)
        c.headers["Authorization"] = f"Bearer {token}"
        yield c
    Base.metadata.drop_all(bind=engine)
    engine.dispose()


TEST_CONDITIONS = ["TEST_CONDITION_1", "TEST_CONDITION_2", "TEST_CONDITION_3"]
TEST_DISEASES = ["TEST_DISEASE_1", "TEST_DISEASE_2"]

DATA = {
    "id": CLIENT_NUMBER + 1,
    "firstName": "Alex",
    "lastName": "Brown",
    "birthday": "2000-09-16",
    "address": "Street",
    "city": "New York",
    "state": "US",
    "zip": "02232",
    "phone": "+19077653340",
    "email": "client@gmail.com",
    "referring": "referring",
    "conditions": TEST_CONDITIONS,
    "otherCondition": "hvoroba",
    "diseases": TEST_DISEASES,
    "medications": "aspirin",
    "covidTestedPositive": "no",
    "covidVaccine": "null",
    "stressfulLevel": 5,
    "consentMinorChild": False,
    "relationshipChild": "",
}

DATA_CLIENT = {
    "id": CLIENT_NUMBER + 1,
    "first_name": "Alex",
    "last_name": "Brown",
    "phone": "+19077653340",
    "email": "client@gmail.com",
}


def test_registration_client(client: TestClient):
    def get_clients_number() -> int:
        #  get Clients
        response = client.get("/api/client/clients")
        assert response
        assert response.ok
        data = response.json()
        assert data
        return len(data)

    clients_number_before = get_clients_number()

    # 1. add Client into DB (client_data)
    response = client.post("/api/client/registration", json=DATA)
    assert response
    assert response.ok

    # 2. Check db
    client_db = Client.query.filter(Client.email == DATA["email"]).first()
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

    client_number_after = get_clients_number()

    assert clients_number_before == client_number_after - 1


def test_doctor_put_client_in_queue(client: TestClient):
    # 1. add Client into DB (client_data)
    response = client.post("/api/client/registration", json=DATA)
    assert response
    assert response.ok
    # 2. Add client for queue
    response = client.post("/api/client/add_clients_queue", json=DATA_CLIENT)
    assert response
    assert response.ok
    # 3. get Queue
    response = client.get("/api/client/queue")
    assert response
    assert response.ok
    data = response.json()
    assert len(data) == 1
    assert data[0]["id"] == 11


def test_get_queue(client: TestClient):
    # 1. create Reception
    doctor = Doctor.query.first()
    reception = Reception(doctor_id=doctor.id).save()
    # 2. add 5 clients in the queue
    for clientDB in Client.query.limit(5).all():
        QueueMember(
            reception_id=reception.id,
            client_id=clientDB.id,
        ).save()
    # 3. get Queue
    response = client.get("/api/client/queue")
    assert response
    assert response.ok
    data = response.json()
    assert data
    assert len(data) == 5


def test_get_client_intake_from_kiosk(client: TestClient):
    clientDB: Client = Client.query.first()
    # 1. add patient in queue
    phone = {"phone": clientDB.phone}
    response = client.post("/api/client/kiosk", json=phone)
    assert response.ok
    # 2. get client for intake
    data = {"api_key": clientDB.api_key, "rougue_mode": True}
    response = client.post("/api/client/client_intake", json=data)
    assert response
    assert response.ok
    data = response.json()
    assert data
    assert data["id"] == clientDB.id

    visit: Visit = Visit.query.first()
    assert visit
    assert visit.client_id == clientDB.id
    assert not visit.end_time
    doctor = Doctor.query.first()
    assert visit.doctor_id == doctor.id

    api_key = clientDB.api_key

    response = client.get(f"/api/client/client_intake/{api_key}")
    assert response
    assert response.ok
    data = response.json()
    assert data
    assert data["id"] == clientDB.id


def test_get_client_intake_add_doctor(client: TestClient):
    # 1. add Client into DB (client_data)
    response = client.post("/api/client/registration", json=DATA)
    assert response
    assert response.ok

    client_intake: Client = Client.query.filter(Client.id == DATA["id"]).first()

    # 2. doctor add patient in queue
    response = client.post("/api/client/add_clients_queue", json=DATA_CLIENT)
    assert response
    assert response.ok

    # 3. get client for intake
    data = {"api_key": client_intake.api_key, "rougue_mode": True}
    response = client.post("/api/client/client_intake", json=data)
    assert response
    assert response.ok
    data = response.json()
    assert data
    assert data["id"] == DATA_CLIENT["id"]

    visit: Visit = Visit.query.first()
    assert visit
    assert visit.client_id == client_intake.id
    assert not visit.end_time
    doctor = Doctor.query.first()
    assert visit.doctor_id == doctor.id

    response = client.get(f"/api/client/client_intake/{client_intake.api_key}")
    assert response
    assert response.ok
    data = response.json()
    assert data
    assert data["id"] == client_intake.id


def test_delete_client_from_queue(client: TestClient):
    # 1. add Client into DB (client_data)
    response = client.post("/api/client/registration", json=DATA)
    assert response
    assert response.ok

    req_client: Client = Client.query.filter(Client.id == DATA["id"]).first()

    # 2. doctor add patient in queue
    response = client.post("/api/client/add_clients_queue", json=DATA_CLIENT)
    assert response
    assert response.ok

    client_data = {
        "id": req_client.id,
        "api_key": req_client.api_key,
        "first_name": req_client.first_name,
        "last_name": req_client.last_name,
        "phone": req_client.phone,
        "email": req_client.email,
    }

    # 3. doctor delete patient from queue
    response = client.post("/api/client/delete_clients_queue", json=client_data)
    assert response
    assert response.ok


def test_identify_client_with_phone(client: TestClient):
    #  Client with phone
    clientDB = Client.query.first()
    phone = {"phone": clientDB.phone}
    response = client.post("/api/client/kiosk", json=phone)
    assert response
    assert response.ok
    data = response.json()
    assert data
    assert data["id"] == clientDB.id
    assert data["phone"] == clientDB.phone


def test_get_client_with_phone(client: TestClient):
    #  get Client with phone
    clientDB = Client.query.first()
    phone = clientDB.phone
    response = client.get(f"/api/client/kiosk/{phone}")
    assert response
    assert response.ok
    data = response.json()
    assert data
    assert data["phone"] == clientDB.phone
