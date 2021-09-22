import pytest
import tests.setup_flask  # noqa: F401

from admin import db, create_app
from admin import mail
from app.models import Doctor

TEST_SENDER = "test_sender"
TEST_EMAIL = "test@mail.com"


@pytest.fixture
def client():
    app = create_app(environment="testing")
    app.config["TESTING"] = True

    with app.test_client() as client:
        app_ctx = app.app_context()
        app_ctx.push()
        db.drop_all()
        db.create_all()
        yield client
        db.session.remove()
        db.drop_all()
        app_ctx.pop()


def test_mail_message(client):
    new_doctor = dict(
        first_name="test_first_name",
        last_name="test_last_name",
        email=TEST_EMAIL,
        role="Doctor",
    )

    with mail.record_messages() as outbox:
        response = client.post("/admin/doctor/new/", data=new_doctor)
        assert response.status_code == 302
        doc: Doctor = Doctor.query.filter(Doctor.email == TEST_EMAIL).first()
        assert doc
        assert len(outbox) == 1
        letter = outbox[0]
        assert doc.api_key in letter.body
        assert letter.subject
