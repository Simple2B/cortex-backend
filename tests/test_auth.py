import pytest
from typing import Generator
from fastapi.testclient import TestClient

import tests.setup  # noqa: F401
from app.database import engine, Base

from app.setup import create_app
from app.models import Doctor


@pytest.fixture()
def client() -> Generator:
    app = create_app()
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    with TestClient(app) as c:
        yield c
    Base.metadata.drop_all(bind=engine)
    engine.dispose()


def test_auth(client: TestClient):
    TEST_EMAIL = "test@email.com"
    TEST_PASS = "password"
    # 1. add Doctor into DB (e-mail, name, api_key)
    doc = Doctor(
        first_name="TestFirstName",
        last_name="TestLastName",
        email=TEST_EMAIL,
    ).save(True)
    # 2. send password to backend
    data = {"api_key": doc.api_key, "password": TEST_PASS}
    response = client.post("/api/auth/sign_up", json=data)
    assert response
    assert response.ok

    # 3. Try login
    data = dict(
        grant_type="password",
        username=TEST_EMAIL,
        password=TEST_PASS,
    )
    response = client.post("/api/auth/sign_in", data=data)
    assert response
    assert response.ok
    assert b'"access_token"' in response.content
    token = response.json()["access_token"]

    # 4. Try to request doctor info
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("api/auth/doctor", headers=headers)
    assert response
    assert response.ok
    assert b'"first_name"' in response.content
    assert response.json()["email"] == TEST_EMAIL


def test_doctor_register_wrong_api_key(client: TestClient):
    TEST_EMAIL = "test@email.com"
    TEST_PASS = "password"
    # 1. add Doctor into DB (e-mail, name, api_key)
    Doctor(
        first_name="TestFirstName",
        last_name="TestLastName",
        email=TEST_EMAIL,
    ).save(True)
    # 2. send password to backend with wrong key
    data = {"api_key": "dummy", "password": TEST_PASS}
    response = client.post("/api/auth/sign_up", json=data)
    assert response.status_code == 404


def test_doctor_login_wrong_password(client: TestClient):
    TEST_EMAIL = "test@email.com"
    TEST_PASS = "password"
    # 1. add Doctor into DB (e-mail, name, api_key)
    doc = Doctor(
        first_name="TestFirstName",
        last_name="TestLastName",
        email=TEST_EMAIL,
        email_approved=True,
    )
    doc.password = TEST_PASS
    # 2. bad login
    data = {"grant_type": "password", "username": TEST_EMAIL, "password": "dummy"}
    response = client.post("/api/auth/sign_in", data=data)
    assert response.status_code == 401
