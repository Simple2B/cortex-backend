from admin.config import BaseConfig as conf


def login(client, email=conf.ADMIN_EMAIL, password=conf.ADMIN_PASSWORD) -> str:
    """get token"""
    data = dict(email=email, password=password)
    response = client.post("/api/auth/sign_in", json=data)
    assert response
    assert response.ok
    assert b'"access_token"' in response.content
    return response.json()["access_token"]


def logout(client):
    raise NotImplementedError()
