


import pytest
from app.services.auth_service import AuthService
from app.security.password import hash_password
from app.domain.models import User


def test_authenticate_user_success(user_repository):
    # Create a test user
    test_user = User(
        username="auth_test_user",
        hashed_password=hash_password("testpassword"),
        role="user"
    )

    user_repository.add(test_user)

    # Initialize AuthService with the repository
    auth_service = AuthService(user_repository)

    # Attempt to authenticate with correct credentials
    token = auth_service.authenticate_user("auth_test_user", "testpassword")

    assert token is not None


def test_authenticate_fail(user_repository):
    auth_service = AuthService(user_repository)

    # Attempt to authenticate with incorrect credentials
    with pytest.raises(Exception):
        auth_service.authenticate_user("unknown_user", "bad")