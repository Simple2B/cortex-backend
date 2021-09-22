import pytest

from admin import db, create_app
from admin import mail
from admin.views import send_email

TEST_SENDER = "test_sender"
TEST_EMAIL = "vsabybina7@mail.com"


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
    data = dict(
        first_name="test_first_name",
        last_name="test_last_name",
        email="test@email.com,",
    )
    response = client.post("admin/doctor/new/", data=data)
    assert response.status_code == 302
    with mail.record_messages() as outbox:

        mail.send_message(subject="testing", body="test", recipients=[TEST_EMAIL])

    assert len(outbox) == 1
    assert outbox[0].subject == "testing"
    send_email()
    assert b" " in response.data
    # send_email()
    # assert b"Confirmation not sent by mail" in response.data
