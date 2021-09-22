import pytest


from admin import db, create_app
from tests.utils import login, logout
from admin.database import add_doctor_to_db


TEST_EMAIL = "test@test.com"
TEST_PASS = "12345"


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


def test_auth_pages(client):
    response = client.get("/admin/login")
    assert response.status_code == 200
    response = client.get("/admin/logout")
    assert response.status_code == 302


def test_login_and_logout(client):
    # Access to logout view before login should fail.
    logout(client)
    doctor = add_doctor_to_db(email=TEST_EMAIL, passwd=TEST_PASS)
    assert doctor
    response = login(client, email=TEST_EMAIL, password=TEST_PASS)
    assert response.status_code == 200
    assert b"Home - Cortex" in response.data
    # Should successfully logout the currently logged in user.
    response = logout(client)
    assert b"You were logged out." in response.data
    # Incorrect login credentials should fail.
    response = login(client, email=TEST_EMAIL, password="wrongpassword")
    assert b"Login V19" in response.data
    response = login(client, email="wrong@gmai.com", password=TEST_PASS)
    assert b"Login V19" in response.data
    response = login(client, email="wrong@gmai.com", password="wrongpassword")
    assert b"Login V19" in response.data
