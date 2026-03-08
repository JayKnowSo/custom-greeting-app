


# tests/test_rbac.py

from fastapi.testclient import TestClient
from jose import jwt
from datetime import datetime, timedelta, timezone

from app.main import app
from app.security.jwt import SECRET_KEY, ALGORITHM


def make_token(username: str, role: str, expired: bool = False) -> str:
    """Mint a test token with any role — no login required."""
    delta = timedelta(minutes=-1) if expired else timedelta(minutes=30)
    payload = {
        "sub": username,
        "role": role,
        "exp": datetime.now(timezone.utc) + delta,
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def auth(token: str) -> dict:
    """Shorthand for Authorization header."""
    return {"Authorization": f"Bearer {token}"}


# ── 401 TESTS — token problems ─────────────────────────────────────

def test_no_token_returns_401(client):
    response = client.post("/sessions", json={
        "username": "test", "greetings": 1, "number": 2, "farewell": "bye"
    })
    assert response.status_code == 401


def test_expired_token_returns_401(client):
    token = make_token("alice", "user", expired=True)
    response = client.post("/sessions",
        json={"username": "test", "greetings": 1, "number": 2, "farewell": "bye"},
        headers=auth(token)
    )
    assert response.status_code == 401


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

def test_readonly_cannot_create_session(client):
    """readonly must be blocked from POST /sessions — this is the attack."""
    token = make_token("bob", "readonly")
    response = client.post("/sessions",
        json={"username": "test", "greetings": 1, "number": 2, "farewell": "bye"},
        headers=auth(token)
    )
    assert response.status_code == 403


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


def test_fake_role_is_denied_everywhere(client):
    """An invented role gets nothing."""
    token = make_token("hacker", "superadmin_fake")
    assert client.post("/sessions",
        json={"username": "test", "greetings": 1, "number": 2, "farewell": "bye"},
        headers=auth(token)
    ).status_code == 403
    assert client.get("/clear", headers=auth(token)).status_code == 403


# ── 200 TESTS — correct role gets through ─────────────────────────

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