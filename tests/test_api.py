

from app.domain.models import User
from app.security.password import hash_password


def test_create_session(client, user_repository):

    # Create test user
    user = User(
        username="testuser",
        hashed_password=hash_password("testpassword"),
        role="user"
    )
    user_repository.add(user)

    # Login to get token
    login = client.post(
        "/login",
        json={"username": "testuser", "password": "testpassword"}
    )
    assert login.status_code == 200
    token = login.json()["access_token"]

    # Call protected endpoint
    response = client.post(
        "/sessions",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "username": "integration_user",
            "greetings": 3,
            "number": 5,
            "farewell": "See you!"
        }
    )

    assert response.status_code == 201

    data = response.json()

    assert data["username"] == "integration_user"
    assert data["number"] == 5


def test_protected_create_session(client, user_repository):

    # Create test user
    user = User(
        username="secure_user",
        hashed_password=hash_password("testpassword"),
        role="user"
    )
    user_repository.add(user)

    # Login
    login = client.post(
        "/login",
        json={"username": "secure_user", "password": "testpassword"}
    )
    
    assert login.status_code == 200, login.text

    token = login.json()["access_token"]

    # Use token
    response = client.post(
        "/sessions",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "username": "secure_test",
            "greetings": 1,
            "number": 2,
            "farewell": "bye"
        }
    )

    assert response.status_code == 201