import pytest
import asyncio
from typing import Generator
from fastapi.testclient import TestClient
from tortoise.contrib.test import finalizer, initializer

from app.setup import create_app
from app.models import User


@pytest.fixture()
def client() -> Generator:
    app = create_app()
    initializer(["app.models"], "sqlite://:memory:")
    with TestClient(app) as c:
        yield c
    finalizer()


@pytest.fixture()
def event_loop(client: TestClient) -> Generator:
    yield client.task.get_loop()


def test_auth(client: TestClient, event_loop: asyncio.AbstractEventLoop):
    data = {"username": "michaelC", "password": "secret"}
    response = client.post("/auth/sign_up", json=data)
    assert response
    assert response.ok
    user = event_loop.run_until_complete(User.filter(username=data["username"]).first())
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
