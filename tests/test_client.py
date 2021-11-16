import pytest
import datetime
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

DATA_FULL_INFO = {
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
    response = client.post("/api/client/registration", json=DATA_FULL_INFO)
    assert response
    assert response.ok

    # 2. Check db
    client_db = Client.query.filter(Client.email == DATA_FULL_INFO["email"]).first()
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
    response = client.post("/api/client/registration", json=DATA_FULL_INFO)
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
    count = 1
    for clientDB in Client.query.limit(5).all():
        QueueMember(reception_id=reception.id, client_id=clientDB.id).save()
        count = count + 1
    # 3. get Queue
    response = client.get("/api/client/queue")
    assert response
    assert response.ok
    queue_data = response.json()
    assert queue_data
    assert len(queue_data) == 5

    member = QueueMember.query.filter(QueueMember.reception_id == reception.id).first()

    client_intake: Client = Client.query.filter(Client.id == member.client_id).first()

    # 4. post client for intake (create visit)
    data = {
        "api_key": client_intake.api_key,
        "rougue_mode": False,
        # "place_in_queue": client_intake.client_info["place_in_queue"],
    }
    response = client.post("/api/client/client_intake", json=data)
    assert response
    assert response.ok
    data = response.json()
    assert data
    assert data["id"] == client_intake.id

    visit: Visit = Visit.query.first()
    assert visit
    assert visit.client_id == client_intake.id
    assert not visit.end_time
    doctor = Doctor.query.first()
    assert visit.doctor_id == doctor.id

    # 5. get client intake
    response = client.get(f"/api/client/client_intake/{client_intake.api_key}")
    assert response
    assert response.ok
    data = response.json()
    assert data
    assert data["id"] == client_intake.id

    # 6. end_date for visit
    data = {
        "api_key": client_intake.api_key,
        "rougue_mode": False,
        # "place_in_queue": client_intake.client_info["place_in_queue"],
    }
    response = client.post("/api/client/complete_client_visit", json=data)
    assert response
    assert response.ok

    # 7. add client_intake in the queue again

    queue_member = {
        "id": client_intake.id,
        "first_name": client_intake.first_name,
        "last_name": client_intake.last_name,
        "phone": client_intake.phone,
        "email": client_intake.email,
    }

    assert queue_member

    response = client.post("/api/client/add_clients_queue", json=queue_member)
    assert response
    assert response.ok

    # 8. get Queue again
    response = client.get("/api/client/queue")
    assert response
    assert response.ok
    data = response.json()
    assert data
    assert len(data) == 5

    client_data = {
        "id": client_intake.id,
        "api_key": client_intake.api_key,
        "first_name": client_intake.first_name,
        "last_name": client_intake.last_name,
        "phone": client_intake.phone,
        "email": client_intake.email,
        # "place_in_queue": client_intake.client_info["place_in_queue"],
    }

    # 9. doctor delete patient from queue
    response = client.post("/api/client/delete_clients_queue", json=client_data)
    assert response
    assert response.ok

    # 10. get Queue again without delete member
    response = client.get("/api/client/queue")
    assert response
    assert response.ok
    data = response.json()
    assert data
    assert len(data) == 4


def test_get_client_intake_from_kiosk(client: TestClient):
    clientDB: Client = Client.query.first()
    # 1. add patient in queue
    phone: object = {"phone": clientDB.phone}
    response = client.post("/api/client/kiosk", json=phone)
    assert response.ok
    # 2. get client for intake
    data = {"api_key": clientDB.api_key, "rougue_mode": False}
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
    response = client.post("/api/client/registration", json=DATA_FULL_INFO)
    assert response
    assert response.ok

    client_intake: Client = Client.query.filter(
        Client.id == DATA_FULL_INFO["id"]
    ).first()

    # 2. doctor add patient in queue
    response = client.post("/api/client/add_clients_queue", json=DATA_CLIENT)
    assert response
    assert response.ok

    # 3. get client for intake
    data = {"api_key": client_intake.api_key, "rougue_mode": False}
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
    req_client: Client = Client.query.first()
    client_data = {
        "id": req_client.id,
        "api_key": req_client.api_key,
        "first_name": req_client.first_name,
        "last_name": req_client.last_name,
        "phone": req_client.phone,
        "email": req_client.email,
    }

    # 2. doctor add patient in queue
    response = client.post("/api/client/add_clients_queue", json=client_data)
    assert response
    assert response.ok

    # 3. doctor delete patient from queue
    response = client.post("/api/client/delete_clients_queue", json=client_data)
    assert response
    assert response.ok


def test_delete_member_from_queue(client: TestClient):
    # 1. create Reception
    doctor = Doctor.query.first()
    reception: Reception = Reception(doctor_id=doctor.id).save(True)
    # 2. add 5 clients in the queue
    for clientDB in Client.query.limit(5).all():
        QueueMember(
            reception_id=reception.id,
            client_id=clientDB.id,
        ).save(True)
    # 3. get Queue
    response = client.get("/api/client/queue")
    assert response
    assert response.ok
    data = response.json()
    assert data
    assert len(data) == 5

    reception_member = reception.queue_members[1]

    member = Client.query.filter(Client.id == reception_member.id).first()

    client_data = {
        "id": member.id,
        "api_key": member.api_key,
        "first_name": member.first_name,
        "last_name": member.last_name,
        "phone": member.phone,
        "email": member.email,
    }

    # 4. doctor delete patient from queue
    response = client.post("/api/client/delete_clients_queue", json=client_data)
    assert response
    assert response.ok

    # 5. get queue after delete
    response = client.get("/api/client/queue")
    assert response
    assert response.ok
    data = response.json()
    assert data
    assert len(data) == 4


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


def test_complete_client_visit(client: TestClient):
    # complete visit (add end_date to visit)

    # 1. add Client into DB (client_data)
    response = client.post("/api/client/registration", json=DATA_FULL_INFO)
    assert response
    assert response.ok

    client_intake: Client = Client.query.filter(
        Client.id == DATA_FULL_INFO["id"]
    ).first()

    # 2. doctor add patient in queue
    response = client.post("/api/client/add_clients_queue", json=DATA_CLIENT)
    assert response
    assert response.ok

    # 3. get client for intake (create visit)
    data = {"api_key": client_intake.api_key, "rougue_mode": False}
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

    # 4. end_date for visit
    data = {"api_key": client_intake.api_key, "rougue_mode": False}
    response = client.post("/api/client/complete_client_visit", json=data)
    assert response
    assert response.ok

    doctor = Doctor.query.first()
    # 5. add 3 visits
    date = datetime.date.today()
    time = datetime.datetime.utcnow().strftime("%m/%d/%Y, %H:%M:%S")
    count = 1
    for clientDB in Client.query.limit(3).all():
        Visit(
            date=date + datetime.timedelta(days=count),
            start_time=datetime.datetime.strptime(time, "%m/%d/%Y, %H:%M:%S")
            + datetime.timedelta(days=count),
            end_time=datetime.datetime.strptime(time, "%m/%d/%Y, %H:%M:%S")
            + datetime.timedelta(days=count + 2),
            client_id=clientDB.id,
            doctor_id=doctor.id,
        ).save()
        count = count + 1

    visit: Visit = Visit.query.all()
    assert visit

    visit1: Visit = Visit.query.first()
    assert visit1
    visit3: Visit = Visit.query.get(3)
    assert visit3

    # 6. get visits for report
    data = {
        "type": "visit",
        "start_time": visit1.start_time.strftime("%m/%d/%Y, %H:%M:%S"),
        "end_time": visit3.end_time.strftime("%m/%d/%Y, %H:%M:%S"),
    }
    # 7. put date for filter report visits
    response = client.post("/api/client/report_visit", json=data)
    assert response
    assert response.ok
    # assert response.text

    # 8. get report with visits
    response = client.get("/api/client/report_visit")
    assert response
    assert response.ok

    # 9. get new clients for report
    data = {
        "type": "new clients",
        "start_time": visit1.start_time.strftime("%m/%d/%Y, %H:%M:%S"),
        "end_time": visit3.end_time.strftime("%m/%d/%Y, %H:%M:%S"),
    }

    response = client.post("/api/client/report_new_clients", json=data)
    assert response
    assert response.ok

    # 10. get report with new client
    response = client.get("/api/client/report_new_clients")
    assert response
    assert response.ok


def test_write_note(client: TestClient):
    #  get notes for client

    client_intake: Client = Client.query.first()

    data_client = {
        "api_key": client_intake.api_key,
        "id": client_intake.id,
        "first_name": client_intake.first_name,
        "last_name": client_intake.last_name,
        "phone": client_intake.phone,
        "email": client_intake.email,
    }

    # 1. doctor add patient in queue
    response = client.post("/api/client/add_clients_queue", json=data_client)
    assert response
    assert response.ok

    # 2. get client for intake (create visit and note)
    data_client_intake = {"api_key": client_intake.api_key, "rougue_mode": False}
    response = client.post("/api/client/client_intake", json=data_client_intake)
    assert response
    assert response.ok
    data_intake = response.json()
    assert data_intake

    visit: Visit = Visit.query.first()
    assert visit
    assert visit.client_id == client_intake.id
    assert not visit.end_time
    doctor = Doctor.query.first()
    assert visit.doctor_id == doctor.id

    response = client.get(f"/api/client/client_intake/{client_intake.api_key}")
    assert response
    assert response.ok
    data_intake = response.json()
    assert data_intake
    assert data_intake["id"] == client_intake.id

    doctor = Doctor.query.first()

    data_note = {
        # "date": visit.date.strftime("%m/%d/%Y"),
        "notes": "New Notes",
        "client_id": visit.client_id,
        "doctor_id": visit.doctor_id,
        "visit_id": visit.id,
    }

    # get visit for note
    response = client.post("/api/client/note", json=data_note)
    assert response
    assert response.ok
    data_note = response.json()
    assert data_note
