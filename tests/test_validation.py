# tests/test_validation.py
from fastapi.testclient import TestClient
from jose import jwt
from datetime import datetime, timedelta, timezone
from app.main import app
from app.security.jwt import SECRET_KEY, ALGORITHM

client = TestClient(app)


def make_token(username: str, role: str) -> str:
    payload = {
        "sub": username,
        "role": role,
        "exp": datetime.now(timezone.utc) + timedelta(minutes=30),
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def auth(token: str) -> dict:
    return {"Authorization": f"Bearer {token}"}


# ── FIELD LENGTH TESTS ─────────────────────────────────────────────

def test_username_too_long_rejected(client):
    """Username over 50 chars must be rejected."""
    token = make_token("alice", "user")
    response = client.post("/sessions",
        json={
            "username": "a" * 51,
            "greetings": 1,
            "number": 2,
            "farewell": "bye"
        },
        headers=auth(token)
    )
    assert response.status_code == 422


def test_empty_username_rejected(client):
    """Empty username must be rejected."""
    token = make_token("alice", "user")
    response = client.post("/sessions",
        json={
            "username": "",
            "greetings": 1,
            "number": 2,
            "farewell": "bye"
        },
        headers=auth(token)
    )
    assert response.status_code == 422


def test_negative_greetings_rejected(client):
    """Negative greetings must be rejected."""
    token = make_token("alice", "user")
    response = client.post("/sessions",
        json={
            "username": "alice",
            "greetings": -1,
            "number": 2,
            "farewell": "bye"
        },
        headers=auth(token)
    )
    assert response.status_code == 422


def test_negative_number_rejected(client):
    """Negative number must be rejected."""
    token = make_token("alice", "user")
    response = client.post("/sessions",
        json={
            "username": "alice",
            "greetings": 1,
            "number": -1,
            "farewell": "bye"
        },
        headers=auth(token)
    )
    assert response.status_code == 422


# ── INJECTION TESTS ────────────────────────────────────────────────

def test_script_tag_in_username_rejected(client):
    """Script tag injection attempt must be rejected."""
    token = make_token("alice", "user")
    response = client.post("/sessions",
        json={
            "username": "<script>alert(1)</script>",
            "greetings": 1,
            "number": 2,
            "farewell": "bye"
        },
        headers=auth(token)
    )
    assert response.status_code == 422


def test_sql_injection_in_username_rejected(client):
    """SQL injection attempt must be rejected."""
    token = make_token("alice", "user")
    response = client.post("/sessions",
        json={
            "username": "alice'; DROP TABLE users;--",
            "greetings": 1,
            "number": 2,
            "farewell": "bye"
        },
        headers=auth(token)
    )
    assert response.status_code == 422


# ── EXTRA FIELDS TEST ──────────────────────────────────────────────

def test_extra_fields_rejected(client):
    """Unknown fields must be rejected — no probing allowed."""
    token = make_token("alice", "user")
    response = client.post("/sessions",
        json={
            "username": "alice",
            "greetings": 1,
            "number": 2,
            "farewell": "bye",
            "is_admin": True,
            "role": "admin"
        },
        headers=auth(token)
    )
    assert response.status_code == 422


# ── LOGIN VALIDATION TESTS ─────────────────────────────────────────

def test_short_password_rejected(client):
    """Password under 8 characters must be rejected."""
    response = client.post("/login",
        json={"username": "alice", "password": "short"}
    )
    assert response.status_code == 422


def test_extra_field_in_login_rejected(client):
    """Extra fields in login must be rejected."""
    response = client.post("/login",
        json={
            "username": "alice",
            "password": "validpassword123",
            "remember_me": True
        }
    )
    assert response.status_code == 422