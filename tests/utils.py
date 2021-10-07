from admin.config import BaseConfig as conf


# fastapi - > login
def login(client, email=conf.ADMIN_EMAIL, password=conf.ADMIN_PASSWORD) -> str:
    """get token"""
    data = dict(email=email, password=password)
    response = client.post("/api/auth/sign_in", json=data)
    assert response
    assert response.ok
    assert b'"access_token"' in response.content
    return response.json()["access_token"]


# fastapi - > logout
def logout(client):
    raise NotImplementedError()


# flask - > login
def admin_login(client, email, password="123"):
    return client.post(
        "/admin/login", data=dict(email=email, password=password), follow_redirects=True
    )


# flask - > logout
def admin_logout(client):
    return client.get("/admin/logout", follow_redirects=True)
