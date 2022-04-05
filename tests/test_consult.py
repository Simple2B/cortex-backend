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

from app.schemas import (
    Consult
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


def test_write_consult(client: TestClient):
    client_consult: TestClient = Client.query.first()

    data_client = {
        "api_key": client_consult.api_key,
        "id": client_consult.id,
        "first_name": client_consult.first_name,
        "last_name": client_consult.last_name,
        "phone": client_consult.phone,
        "email": client_consult.email,
}

    # 1. doctor add patient in queue
    response = client.post("/api/client/add_clients_queue", json=data_client)
    assert response
    assert response.ok

    # 2. get client for intake (create visit and note)
    data_client_intake = {"api_key": client_consult.api_key, "rougue_mode": False}
    response = client.post("/api/client/client_intake", json=data_client_intake)
    assert response
    assert response.ok
    data_intake = response.json()
    assert data_intake

    # 2. post client consult
    data_client_intake = {
        "consult": "test4",
        "client_id": 1,
        "doctor_id": 1,
        "visit_id": 2,
    }

    response = client.post("/api/consult/write_consult", json=data_client_intake)
    assert response
    assert response.ok
    data_consult = response.json()
    assert data_consult

    # 2. get client consult
    response = client.get(f"/api/consult/get_consult/{client_consult.api_key}")
    assert response
    assert response.ok
    get_data_consult = response.json()
    assert get_data_consult


    response = client.post("/api/consult/consult_delete/", json=data_consult)
    assert response
    assert response.ok
