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
    client_intake
    data = {
        "api_key": client_intake.api_key,
        "date": "11/22/2021, 11:43:14",
    }
    response = client.post("/api/test/test", json=data)
    assert response
    assert response.ok
    data_start_test = response.json()
    assert data_start_test
    assert data_start_test["client_id"] == client_intake.id
