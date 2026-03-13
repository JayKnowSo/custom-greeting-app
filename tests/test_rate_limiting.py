# This test suite is designed to verify that the rate limiting functionality of the
# API is working as intended.
# It uses the TestClient from FastAPI to make requests to the API endpoints and
# checks that the correct status codes are returned when the rate limits are exceeded.
# The tests cover the /login, /sessions, /sessions/search, and /clear endpoints,
# ensuring that they all enforce their respective rate limits to prevent
# abuse and protect the application from excessive requests.
# The make_token and auth helper functions are used to create JWT tokens and
# set up the Authorization header for the test requests, allowing the tests to
# simulate authenticated requests to the protected endpoints.


# tests/test_rate_limiting.py
from fastapi.testclient import TestClient
from jose import jwt
from datetime import datetime, timedelta, timezone
from app.main import app, limiter
from app.security.jwt import SECRET_KEY, ALGORITHM

client = TestClient(app, raise_server_exceptions=False)


def make_token(username: str, role: str) -> str:
    payload = {
        "sub": username,
        "role": role,
        "exp": datetime.now(timezone.utc) + timedelta(minutes=30),
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def auth(token: str) -> dict:
    return {"Authorization": f"Bearer {token}"}


def enable_limiter():
    limiter.enabled = True


def cleanup_limiter():
    """Disable and wipe all hit counts."""
    limiter.enabled = False
    try:
        limiter._storage.storage.clear()
    except Exception:
        pass


def test_login_rate_limit_blocks_after_5_requests():
    enable_limiter()
    try:
        payload = {"username": "test", "password": "wrongpassword"}
        responses = [client.post("/login", json=payload) for _ in range(6)]
        assert responses[5].status_code == 429
    finally:
        cleanup_limiter()


def test_session_rate_limit_blocks_after_30_requests():
    enable_limiter()
    try:
        token = make_token("alice", "user")
        payload = {"username": "alice", "greetings": 1, "number": 2, "farewell": "bye"}
        responses = [
            client.post("/sessions", json=payload, headers=auth(token))
            for _ in range(31)
        ]
        assert responses[30].status_code == 429
    finally:
        cleanup_limiter()


def test_search_rate_limit_blocks_after_30_requests():
    enable_limiter()
    try:
        token = make_token("alice", "user")
        responses = [
            client.get("/sessions/search?username=alice", headers=auth(token))
            for _ in range(31)
        ]
        assert responses[30].status_code == 429
    finally:
        cleanup_limiter()


def test_clear_rate_limit_blocks_after_10_requests():
    enable_limiter()
    try:
        token = make_token("superuser", "admin")
        responses = [
            client.get("/clear", headers=auth(token))
            for _ in range(11)
        ]
        assert responses[10].status_code == 429
    finally:
        cleanup_limiter()
