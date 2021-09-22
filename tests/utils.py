def login(client, email, password="123"):
    return client.post(
        "/admin/login", data=dict(email=email, password=password), follow_redirects=True
    )


def logout(client):
    return client.get("/admin/logout", follow_redirects=True)
