# tests/test_auth_api.py
# This file contains tests for the authentication API endpoints of the application.
# The tests verify that the login functionality works correctly,
# including successful logins and handling of invalid credentials.
# It uses the test client provided by FastAPI to simulate HTTP requests to the API.

from app.security.password import hash_password
from app.domain.models import User


def test_login_success(client, user_repository):

    # create user in test DB
    test_user = User(
        username="auth_test_user",
        hashed_password=hash_password("testpassword"),
        role="user"
    )

    user_repository.add(test_user)

    # attempt login
    response = client.post(
        "/login",
        json={"username": "auth_test_user", "password": "testpassword"}
    )

    assert response.status_code == 200
    assert "access_token" in response.json()
