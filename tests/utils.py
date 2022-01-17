# from fastapi import Depends, HTTPException
# from fastapi.security import OAuth2PasswordRequestForm
from admin.config import BaseConfig as conf


# fastapi - > login
def login(client, username=conf.ADMIN_EMAIL, password=conf.ADMIN_PASSWORD) -> str:
    """get token"""
    data = dict(
        grant_type="password",
        username=username,
        password=password,
        scope="",
        client_id="",
        client_secret="",
    )
    response = client.post("/api/auth/sign_in", data=data)
    assert response
    assert response.ok
    assert b'"access_token"' in response.content
    return response.json()["access_token"]


# fastapi - > login
# def login(client, form_data: OAuth2PasswordRequestForm = Depends()) -> str:
#     """get token"""

#     user_dict = client.get(form_data.username)
#     if not user_dict:
#         raise HTTPException(status_code=400, detail="Incorrect username or password")
#     response = client.post("/api/auth/sign_in", json=user_dict)
#     assert response
#     assert response.ok
#     assert b'"access_token"' in response.content
#     return response.json()["access_token"]


# # fastapi - > logout
# def logout(client):
#     raise NotImplementedError()


# flask - > login
def admin_login(client, email, password="123"):
    return client.post(
        "/admin/login", data=dict(email=email, password=password), follow_redirects=True
    )


# flask - > logout
def admin_logout(client):
    return client.get("/admin/logout", follow_redirects=True)
