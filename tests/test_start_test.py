import pytest
from typing import Generator
from fastapi.testclient import TestClient

import tests.setup  # noqa: F401
from app.database import engine, Base

from app.setup import create_app
from app.models import Client

from .database import generate_test_data
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


def test_create_start_test(client: TestClient):
    client_intake: Client = Client.query.first()
    data = {
        "api_key": client_intake.api_key,
        "date": "11/22/2021, 11:43:14",
    }
    response = client.post("/api/test/test_create", json=data)
    assert response
    assert response.ok
    data_start_test = response.json()
    assert data_start_test
    assert data_start_test["client_id"] == client_intake.id


def test_get_client_tests(client: TestClient):
    client_intake: Client = Client.query.first()

    dates = ["9/10/2021, 11:43:14", "10/12/2021, 11:43:14", "11/22/2021, 11:43:14"]

    for date in dates:

        data = {
            "api_key": client_intake.api_key,
            "date": date,
        }

        response = client.post("/api/test/test_create", json=data)
        assert response
        assert response.ok

    response = client.get(f"/api/test/client_tests/{client_intake.api_key}")
    assert response
    assert response.ok
    data_start_test = response.json()
    assert len(data_start_test) == 3


def test_write_care_plan_frequency(client: TestClient):
    client_intake: Client = Client.query.first()
    data = {
        "api_key": client_intake.api_key,
        "date": "11/22/2021, 11:43:14",
    }
    # 1. create test for client
    response = client.post("/api/test/test_create", json=data)
    assert response
    assert response.ok
    data_start_test = response.json()
    assert data_start_test
    assert data_start_test["client_id"] == client_intake.id

    data_for_test = {
        "test_id": data_start_test["id"],
        "api_key": client_intake.api_key,
        "care_plan": "3-month",
        "frequency": "1-month",
    }
    # 2. write care plan to created test
    response = client.post("/api/test/care_plan_frequency", json=data_for_test)
    assert response
    assert response.ok
    test_data = response.json()
    assert test_data
    assert test_data["care_plan"] == "3-month"
    assert test_data["frequency"] == "1-month"

    # 3. get all names of care plan
    response = client.get("/api/test/care_plan_names")
    assert response
    assert response.ok
    data_names_care_plan = response.json()
    assert data_names_care_plan
    assert len(data_names_care_plan) == 1
    assert data_names_care_plan[0]["care_plan"] == "3-month"

    #  4. get tests with care plan
    response = client.get(f"/api/test/client_tests/{client_intake.api_key}")
    assert response
    assert response.ok
    data_test_with_care_plan = response.json()
    assert data_test_with_care_plan

    test_id = test_data["id"]

    # 5. get test with test_id
    response = client.get(f"/api/test/test/{test_id}")
    assert response
    assert response.ok
