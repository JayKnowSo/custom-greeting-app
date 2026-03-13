


# tests/test_rbac.py
# This file contains tests for the RBAC implementation in app.security.rbac.
# The tests are organized into three sections:
# 1. Tests that check for 401 Unauthorized responses when the token is missing, expired, or tampered with.
# 2. Tests that check for 403 Forbidden responses when the user has the wrong role for the action they are trying to perform.
# 3. Tests that check for 200 OK responses when the user has the correct role for the action they are trying to

from jose import jwt
from datetime import datetime, timedelta, timezone

from app.security.jwt import SECRET_KEY, ALGORITHM



# Helper functions for tests
# These functions are used to create tokens and set up the Authorization header for the test requests.

def make_token(username: str, role: str, expired: bool = False) -> str:
    """Mint a test token with any role — no login required."""
    delta = timedelta(minutes=-1) if expired else timedelta(minutes=30)
    payload = {
        "sub": username,
        "role": role,
        "exp": datetime.now(timezone.utc) + delta,
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

# The auth function is a shorthand for creating the Authorization header with a Bearer token.

def auth(token: str) -> dict:
    """Shorthand for Authorization header."""
    return {"Authorization": f"Bearer {token}"}


# ── 401 TESTS — token problems ─────────────────────────────────────
# These tests check that the API correctly returns a 401 Unauthorized status code when the token is missing,
# expired, or tampered with. This is important for security, as it ensures that only valid tokens can access protected endpoints.

def test_no_token_returns_401(client):
    response = client.post("/sessions", json={
        "username": "test", "greetings": 1, "number": 2, "farewell": "bye"
    })
    assert response.status_code == 401

# The next two tests check that expired tokens and tampered tokens are correctly rejected with a 401 status code.

def test_expired_token_returns_401(client):
    token = make_token("alice", "user", expired=True)
    response = client.post("/sessions",
        json={"username": "test", "greetings": 1, "number": 2, "farewell": "bye"},
        headers=auth(token)
    )
    assert response.status_code == 401

# The test_tampered_token_returns_401 function creates a token with the wrong secret key,
# simulating a tampered token, and checks that it is rejected with a 401 status code.
# This ensures that the API is properly verifying the integrity of the token and not accepting forged tokens.

def test_tampered_token_returns_401(client):
    bad_token = jwt.encode(
        {"sub": "hacker", "role": "admin",
         "exp": datetime.now(timezone.utc) + timedelta(minutes=30)},
        "wrong-secret-key",
        algorithm=ALGORITHM
    )
    response = client.post("/sessions",
        json={"username": "test", "greetings": 1, "number": 2, "farewell": "bye"},
        headers=auth(bad_token)
    )
    assert response.status_code == 401


# ── 403 TESTS — wrong role (the actual attacks) ────────────────────
# These tests check that users with the wrong role are correctly blocked with a 403 Forbidden
# status code when they try to perform actions they are not authorized for.

def test_readonly_cannot_create_session(client):
    """readonly must be blocked from POST /sessions — this is the attack."""
    token = make_token("bob", "readonly")
    response = client.post("/sessions",
        json={"username": "test", "greetings": 1, "number": 2, "farewell": "bye"},
        headers=auth(token)
    )
    assert response.status_code == 403

# The next two tests check that the "readonly" role cannot clear the database
# and that the "user" role cannot access admin-only endpoints.

def test_readonly_cannot_clear_database(client):
    """readonly must never wipe the database."""
    token = make_token("bob", "readonly")
    response = client.get("/clear", headers=auth(token))
    assert response.status_code == 403


def test_user_role_cannot_clear_database(client):
    """user role must be blocked from admin-only /clear."""
    token = make_token("alice", "user")
    response = client.get("/clear", headers=auth(token))
    assert response.status_code == 403

# The test_user_role_cannot_access_admin_endpoints function checks that a user with the
# "user" role cannot access admin-only endpoints, ensuring that the RBAC system is properly enforcing
# role-based access control and preventing unauthorized access to sensitive operations

def test_fake_role_is_denied_everywhere(client):
    """An invented role gets nothing."""
    token = make_token("hacker", "superadmin_fake")
    assert client.post("/sessions",
        json={"username": "test", "greetings": 1, "number": 2, "farewell": "bye"},
        headers=auth(token)
    ).status_code == 403
    assert client.get("/clear", headers=auth(token)).status_code == 403


# ── 200 TESTS — correct role gets through ─────────────────────────
# These tests check that users with the correct role are able to
# access the endpoints they are authorized for.

def test_user_role_can_search_sessions(client):
    token = make_token("alice", "user")
    response = client.get("/sessions/search?username=alice", headers=auth(token))
    assert response.status_code == 200


def test_admin_can_search_sessions(client):
    token = make_token("superuser", "admin")
    response = client.get("/sessions/search?username=alice", headers=auth(token))
    assert response.status_code == 200


def test_admin_inherits_all_access(client):
    """Admin must never be blocked by a lower-level guard."""
    token = make_token("superuser", "admin")
    assert client.get("/sessions/search?username=alice",
                      headers=auth(token)).status_code == 200
    assert client.get("/clear", headers=auth(token)).status_code == 200
