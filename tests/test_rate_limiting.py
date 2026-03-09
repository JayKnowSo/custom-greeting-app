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
from app.main import app
from app.security.jwt import SECRET_KEY, ALGORITHM

# This test suite checks that the rate limits defined in the API routes are properly enforced.
# It uses the TestClient from FastAPI to make requests to the API endpoints and verifies that the correct status codes are returned when the limits are exceeded. 
# The tests cover the /login, /sessions, /sessions/search,
# and /clear endpoints, ensuring that they all enforce their respective rate limits.

client = TestClient(app, raise_server_exceptions=False)

# Helper functions for tests
# These functions are used to create tokens and 
# set up the Authorization header for the test requests.
# The make_token function creates a JWT token with the specified username and role,
# and the auth function formats the Authorization header for use in the test requests.

def make_token(username: str, role: str) -> str:
    payload = {
        "sub": username,
        "role": role,
        "exp": datetime.now(timezone.utc) + timedelta(minutes=30),
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def auth(token: str) -> dict:
    return {"Authorization": f"Bearer {token}"}


# ── LOGIN RATE LIMIT ───────────────────────────────────────────────
# The /login endpoint allows 5 requests per minute per IP address, 
# and this test checks that the 6th request is blocked with a 429 Too Many Requests status code.
# This is a common brute force protection mechanism to 
# prevent attackers from trying to guess passwords by making repeated login attempts.


def test_login_rate_limit_blocks_after_5_requests():
    """
    /login allows 5 requests per minute per IP.
    The 6th request must return 429 Too Many Requests.
    This is brute force protection.
    """
    payload = {"username": "test", "password": "wrongpassword"}

    responses = [
        client.post("/login", json=payload)
        for _ in range(6)
    ]

    status_codes = [r.status_code for r in responses]
    print("Login status codes:", status_codes)

    # First 5 can be 401 (wrong password) or 200 (correct)
    # The 6th must be 429
    assert responses[5].status_code == 429, (
        f"Expected 429 on 6th request, got {responses[5].status_code}"
    )


# ── SESSION RATE LIMIT ─────────────────────────────────────────────
# The /sessions endpoint allows 30 requests per minute per user, 
# and this test checks that the 31st request is blocked with a 429 status code.
# This is important to prevent abuse of the session creation functionality,
# which could lead to resource exhaustion if not properly rate limited.


def test_session_rate_limit_blocks_after_30_requests():
    """
    POST /sessions allows 30 requests per minute.
    The 31st must return 429.
    """
    token = make_token("alice", "user")
    payload = {"username": "alice", "greetings": 1, "number": 2, "farewell": "bye"}

    responses = [
        client.post("/sessions", json=payload, headers=auth(token))
        for _ in range(31)
    ]

    status_codes = [r.status_code for r in responses]
    print("Session status codes:", status_codes)

    assert responses[30].status_code == 429, (
        f"Expected 429 on 31st request, got {responses[30].status_code}"
    )


# ── SEARCH RATE LIMIT ──────────────────────────────────────────────
# The /sessions/search endpoint also has a rate limit of 30 requests per minute,
# and this test checks that it is properly enforced by making 31 requests and expecting a 429 status code on the last one.
# This ensures that users cannot abuse the search functionality by making
# excessive requests.

def test_search_rate_limit_blocks_after_30_requests():
    """
    GET /sessions/search allows 30 requests per minute.
    The 31st must return 429.
    """
    token = make_token("alice", "user")

    responses = [
        client.get("/sessions/search?username=alice", headers=auth(token))
        for _ in range(31)
    ]

    assert responses[30].status_code == 429, (
        f"Expected 429 on 31st request, got {responses[30].status_code}"
    )


# ── CLEAR RATE LIMIT ───────────────────────────────────────────────

# The /clear endpoint is admin-only, but it also has a rate limit of 10 requests per minute.
# This test checks that even an admin user is blocked with a 429 status code after 
# 10 requests, ensuring that the rate limiting is properly enforced as a second line of defense against abuse

def test_clear_rate_limit_blocks_after_10_requests():
    """
    GET /clear allows 10 requests per minute.
    The 11th must return 429.
    Admin role required — rate limit is the second line of defense.
    """
    token = make_token("superuser", "admin")

    responses = [
        client.get("/clear", headers=auth(token))
        for _ in range(11)
    ]

    assert responses[10].status_code == 429, (
        f"Expected 429 on 11th request, got {responses[10].status_code}"
    )