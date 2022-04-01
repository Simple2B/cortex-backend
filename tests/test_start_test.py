import datetime
import pytest
from typing import Generator
from fastapi.testclient import TestClient

import tests.setup  # noqa: F401
from app.database import engine, Base

from app.setup import create_app
from app.models import Client, Doctor, Visit

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


def test_history_care_plan(client: TestClient):
    client_intake: Client = Client.query.first()

    data = {
        "api_key": client_intake.api_key,
        "date": "8/22/2021, 11:43:14",
        "start_time": "05/20/2022, 15:30:00",
        "end_time": "11/08/2022, 12:00:00",
        "care_plan": "6-month",
        "frequency": "1-month",
        "progress_date": "",
        "client_id": 73656,
        "doctor_id": 5314,
        "doctor_name": "Bob Red",
        "tests": "",
        "notes": "",
    }

    # 1. create care plan
    response = client.post("/api/test/care_plan_create", json=data)
    assert response
    assert response.ok
    data_care_plan = response.json()
    assert data_care_plan

    # 2. add end_time to care plan depens on plan
    response = client.post("/api/test/care_plan_create", json=data)
    assert response
    assert response.ok

    # 3. get history plan
    response = client.get(f"/api/test/care_plan_history/{data['api_key']}", json=data)
    assert response
    assert response.ok
    data_care_history_plan = response.json()
    assert data_care_history_plan


def test_create_care_plan(client: TestClient):
    client_intake: Client = Client.query.first()
    data = {
        "api_key": client_intake.api_key,
        "start_time": "05/20/2022, 15:30:00",
    }
    # 1. create care plan
    response = client.post("/api/test/care_plan_create", json=data)
    assert response
    assert response.ok
    data_care_plan = response.json()
    assert data_care_plan

    test_data = {
        "api_key": client_intake.api_key,
        "date": "8/22/2021, 11:43:14",
        "current_care_plan_id": data_care_plan["id"],
    }

    # 2. create test for client
    response = client.post("/api/test/test_create", json=test_data)
    assert response
    assert response.ok
    data_start_test = response.json()
    assert data_start_test
    assert data_start_test["client_id"] == client_intake.id

    # data_for_test = {
    #     "test_id": data_start_test["id"],
    #     "api_key": client_intake.api_key,
    #     "care_plan": "3-month",
    #     "frequency": "1-month",
    # }
    # 3. write to care plan  - plan and frequency
    # response = client.post("/api/test/care_plan_frequency", json=data_for_test)
    # assert response
    # assert response.ok
    # care_plan_data = response.json()
    # assert care_plan_data
    # assert care_plan_data["care_plan"] == "3-month"
    # assert care_plan_data["frequency"] == "1-month"

    # 4. add end_time to care plan depens on plan
    response = client.post("/api/test/care_plan_create", json=data)
    assert response
    assert response.ok

    # 5. get care plan
    response = client.get(f"/api/test/care_plan_create/{client_intake.api_key}")
    assert response
    assert response.ok
    care_plan = response.json() or data
    assert care_plan


def test_create_start_test(client: TestClient):
    client_intake: Client = Client.query.first()
    data_client = {
        "api_key": client_intake.api_key,
        "start_time": "05/20/2022, 15:30:00",
    }
    response = client.post("/api/test/care_plan_create", json=data_client)
    assert response
    assert response.ok
    data_care_plan = response.json()
    assert data_care_plan

    data = {
        "api_key": client_intake.api_key,
        "date": "11/22/2021, 11:43:14",
        "current_care_plan_id": data_care_plan["id"],
    }
    response = client.post("/api/test/test_create", json=data)
    assert response
    assert response.ok
    data_start_test = response.json()
    assert data_start_test


def test_get_client_tests(client: TestClient):
    client_intake: Client = Client.query.first()
    data_client = {
        "api_key": client_intake.api_key,
        "start_time": "05/20/2022, 15:30:00",
    }
    response = client.post("/api/test/care_plan_create", json=data_client)
    assert response
    assert response.ok
    data_care_plan = response.json()
    assert data_care_plan

    dates = ["9/10/2021, 11:43:14", "10/12/2021, 11:43:14", "11/22/2021, 11:43:14"]

    for date in dates:

        data = {
            "api_key": client_intake.api_key,
            "date": date,
            "current_care_plan_id": data_care_plan["id"],
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
    # 1. create care plan for client
    client_intake: Client = Client.query.first()
    data_client = {
        "api_key": client_intake.api_key,
        "start_time": "05/20/2022, 15:30:00",
    }
    response = client.post("/api/test/care_plan_create", json=data_client)
    assert response
    assert response.ok
    data_care_plan = response.json()
    assert data_care_plan

    data = {
        "api_key": client_intake.api_key,
        "date": "11/22/2021, 11:43:14",
        "current_care_plan_id": data_care_plan["id"],
    }
    # 2. create test for client
    response = client.post("/api/test/test_create", json=data)
    assert response
    assert response.ok
    data_start_test = response.json()
    assert data_start_test
    assert data_start_test["client_id"] == client_intake.id

    data_for_test = {
        "test_id": data_start_test["id"],
        "api_key": client_intake.api_key,
        "progress_date": "",
        "care_plan": "3-month",
        "frequency": "1-month",
    }
    # 3. write care plan without date to created test
    # response = client.post("/api/test/care_plan_frequency", json=data_for_test)
    # assert response
    # assert response.ok
    # care_plan_data = response.json()
    # assert care_plan_data
    # assert care_plan_data["care_plan"] == "3-month"
    # assert care_plan_data["frequency"] == "1-month"

    data_for_test = {
        "test_id": data_start_test["id"],
        "api_key": client_intake.api_key,
        "progress_date": "9/10/2021, 11:43:14",
        "care_plan": "3-month",
        "frequency": "1-month",
    }
    # 3-1. write care plan with date to created test
    response = client.post("/api/test/care_plan_frequency", json=data_for_test)
    assert response
    assert response.ok
    care_plan_data = response.json()
    assert care_plan_data
    assert care_plan_data["care_plan"] == "3-month"
    assert care_plan_data["frequency"] == "1-month"

    # 4. get all names of care plan
    response = client.get("/api/test/care_plan_names")
    assert response
    assert response.ok
    data_names_care_plan = response.json()
    assert data_names_care_plan
    assert len(data_names_care_plan) == 1
    assert data_names_care_plan[0]["care_plan"] == "3-month"

    # 5. get all names of frequency
    response = client.get("/api/test/frequency_names")
    assert response
    assert response.ok
    data_names_frequency = response.json()
    assert data_names_frequency
    assert len(data_names_frequency) == 1
    assert data_names_frequency[0]["frequency"] == "1-month"

    # 6. get tests with care plan
    response = client.get(f"/api/test/client_tests/{client_intake.api_key}")
    assert response
    assert response.ok
    data_test_with_care_plan = response.json()
    assert data_test_with_care_plan

    test_id = data_for_test["test_id"]

    # 6. get test with test_id
    response = client.get(f"/api/test/test/{test_id}")
    assert response
    assert response.ok
    test = response.json()
    assert test

    doctor = Doctor.query.first()
    # 2. add 3 visits
    date = datetime.date.today()
    time = datetime.datetime.utcnow().strftime("%m/%d/%Y, %H:%M:%S")
    count = 1
    for i in range(3):
        Visit(
            date=date + datetime.timedelta(days=count),
            start_time=datetime.datetime.strptime(time, "%m/%d/%Y, %H:%M:%S")
            + datetime.timedelta(days=count),
            end_time=datetime.datetime.strptime(time, "%m/%d/%Y, %H:%M:%S")
            + datetime.timedelta(days=i + 2),
            client_id=client_intake.id,
            doctor_id=doctor.id,
        ).save()
        count = count + 1

    visits: Client = client_intake.client_info["visits"]
    assert visits

    # get care plan for client
    response = client.get(f"/api/test/info_for_care_plan_page/{client_intake.api_key}")
    assert response
    assert response.ok
    care_plan_info_tests = response.json()
    assert care_plan_info_tests


def test_get_care_plan_and_frequency_names(client: TestClient):
    # 1. create care plan for client
    client_intake: Client = Client.query.first()
    data_client = {
        "api_key": client_intake.api_key,
        "start_time": "05/20/2022, 15:30:00",
    }
    response = client.post("/api/test/care_plan_create", json=data_client)
    assert response
    assert response.ok
    data_care_plan = response.json()
    assert data_care_plan

    data = {
        "api_key": client_intake.api_key,
        "date": "11/22/2021, 11:43:14",
        "current_care_plan_id": data_care_plan["id"],
    }
    # 2. create test for client
    response = client.post("/api/test/test_create", json=data)
    assert response
    assert response.ok
    data_start_test = response.json()
    assert data_start_test
    assert data_start_test["client_id"] == client_intake.id

    # care_plan_names = ["2-month", "3-month", "1-month", "10-month"]
    # frequency_names = ["6-week", "12-week", "1-week", "10-week"]

    # for i in range(4):
    #     data_for_test = {
    #         "test_id": data_start_test["id"],
    #         "api_key": client_intake.api_key,
    #         "progress_date": "",
    #         "care_plan": care_plan_names[i],
    #         "frequency": frequency_names[i],
    #     }

    # 3. write to care plan names of care plan and frequency
    # response = client.post("/api/test/care_plan_frequency", json=data_for_test)
    # assert response
    # assert response.ok

    # 4. get all names of care plan (magnification filtering)
    response = client.get("/api/test/care_plan_names")
    assert response
    assert response.ok
    data_names_care_plan = response.json()
    assert data_names_care_plan

    # 5. get all names of frequency (magnification filtering)
    response = client.get("/api/test/frequency_names")
    assert response
    assert response.ok
    data_names_frequency = response.json()
    assert data_names_frequency
