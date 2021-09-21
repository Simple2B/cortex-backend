import os
import pytest
import asyncio
from typing import Generator
from fastapi.testclient import TestClient

# flake8: noqa E402
os.environ["FLASK_APP"] = "testing"

from app.database import engine, Base

from app.setup import create_app
from app.models import Doctor


@pytest.fixture()
def client() -> Generator:
    app = create_app()
    Base.metadata.create_all(bind=engine)
    with TestClient(app) as c:
        yield c
    Base.metadata.drop_all(bind=engine)
    engine.dispose()


@pytest.fixture()
def event_loop(client: TestClient) -> Generator:
    yield client.task.get_loop()


def test_auth(client: TestClient, event_loop: asyncio.AbstractEventLoop):
    data = {"email": "test@doctor.com", "password": "secret"}
    response = client.post("/auth/sign_up", json=data)
    assert response
    assert response.ok
    user = event_loop.run_until_complete(Doctor.filter(email=data["email"]).first())
    assert user
    assert user.username == data["username"]

    response = client.post("/auth/sign_in", json=data)
    assert response
    assert response.ok
    assert b'{"access_token"' in response.content
    token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    response = client.get("auth/user", headers=headers)
    assert response
    assert response.ok
    assert b'{"username"' in response.content
