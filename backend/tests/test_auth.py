def test_register_login_me_refresh_and_logout_flow(client):
    register_response = client.post(
        "/api/v1/auth/register",
        json={
            "name": "Test User",
            "email": "test@example.com",
            "password": "supersecret123",
        },
    )

    assert register_response.status_code == 201
    register_payload = register_response.json()
    access_token = register_payload["access_token"]
    assert register_payload["user"]["email"] == "test@example.com"
    assert "book_notes_refresh_token" in register_response.cookies

    me_response = client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {access_token}"})
    assert me_response.status_code == 200
    assert me_response.json()["email"] == "test@example.com"

    refresh_response = client.post("/api/v1/auth/refresh")
    assert refresh_response.status_code == 200
    refreshed_access_token = refresh_response.json()["access_token"]
    assert refreshed_access_token

    refreshed_me_response = client.get(
        "/api/v1/auth/me",
        headers={"Authorization": f"Bearer {refreshed_access_token}"},
    )
    assert refreshed_me_response.status_code == 200
    assert refreshed_me_response.json()["email"] == "test@example.com"

    logout_response = client.post("/api/v1/auth/logout")
    assert logout_response.status_code == 200
    assert logout_response.json()["message"] == "Logged out successfully"


def test_login_rejects_invalid_password(client):
    client.post(
        "/api/v1/auth/register",
        json={
            "name": "Test User",
            "email": "test@example.com",
            "password": "supersecret123",
        },
    )

    login_response = client.post(
        "/api/v1/auth/login",
        json={
            "email": "test@example.com",
            "password": "wrongpass123",
        },
    )

    assert login_response.status_code == 401
    assert login_response.json()["message"] == "Invalid email or password"


def test_register_rejects_duplicate_email(client):
    payload = {
        "name": "Test User",
        "email": "duplicate@example.com",
        "password": "supersecret123",
    }

    first_response = client.post("/api/v1/auth/register", json=payload)
    assert first_response.status_code == 201

    duplicate_response = client.post("/api/v1/auth/register", json=payload)
    assert duplicate_response.status_code == 409
    assert duplicate_response.json()["message"] == "A user with this email already exists"


def test_refresh_token_cannot_be_reused_after_refresh(client):
    register_response = client.post(
        "/api/v1/auth/register",
        json={
            "name": "Refresh User",
            "email": "refresh@example.com",
            "password": "supersecret123",
        },
    )
    original_refresh_token = register_response.cookies["book_notes_refresh_token"]

    refresh_response = client.post("/api/v1/auth/refresh")
    assert refresh_response.status_code == 200
    rotated_refresh_token = refresh_response.cookies["book_notes_refresh_token"]
    assert rotated_refresh_token

    client.cookies.set("book_notes_refresh_token", original_refresh_token)
    reuse_response = client.post("/api/v1/auth/refresh")
    assert reuse_response.status_code == 401
    assert reuse_response.json()["message"] == "Refresh token is no longer valid"


def test_refresh_fails_after_logout(client):
    register_response = client.post(
        "/api/v1/auth/register",
        json={
            "name": "Logout User",
            "email": "logout@example.com",
            "password": "supersecret123",
        },
    )
    refresh_token = register_response.cookies["book_notes_refresh_token"]

    logout_response = client.post("/api/v1/auth/logout")
    assert logout_response.status_code == 200

    client.cookies.set("book_notes_refresh_token", refresh_token)
    refresh_response = client.post("/api/v1/auth/refresh")
    assert refresh_response.status_code == 401
    assert refresh_response.json()["message"] == "Refresh token is no longer valid"
