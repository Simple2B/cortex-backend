import pytest
from typing import Generator
from fastapi.testclient import TestClient

import tests.setup  # noqa: F401
from app.database import engine, Base

from app.setup import create_app

# from app.models import (
#     Client,
#     Doctor,
#     Visit,
#     Reception,
#     QueueMember,
# )
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


# def test_generate_data(client: TestClient):
#     assert len(Client.query.all()) == 10
#     assert len(Doctor.query.all()) == 1
#     assert len(Visit.query.all()) > 0
#     reception = Reception.query.first()
#     assert reception
#     queues = QueueMember.query.all()
#     assert queues
#     assert len(reception.queue_members) == len(queues)

# client = Client.query.first()
# assert client
