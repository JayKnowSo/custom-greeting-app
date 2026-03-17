"""
Phase 1 TDD Checkpoint
Tests marked with @pytest.mark.skipif skip in CI where Docker is unavailable.
"""
import os
import subprocess
import pytest

IN_CI = os.getenv("CI") == "true"


# ── TEST 1: pip CVE remediation ─────────────────────────────────────
@pytest.mark.skipif(IN_CI, reason="requires running Docker container")
def test_pip_version_remediated_in_runtime():
    """pip inside the container must be >= 25.3 to clear CVE-2025-8869."""
    result = subprocess.run(
        ["docker", "exec", "greeting_app", "pip", "--version"],
        capture_output=True, text=True
    )
    assert result.returncode == 0, "Could not exec into container"
    version_str = result.stdout.split()[1]
    major, minor = int(version_str.split(".")[0]), int(version_str.split(".")[1])
    assert (major, minor) >= (25, 3), f"pip {version_str} is vulnerable"


# ── TEST 2: Image digest pinning ────────────────────────────────────
def test_postgres_image_pinned_to_digest():
    """postgres image must be pinned to sha256 digest."""
    with open("docker-compose.yml", "r") as f:
        content = f.read()
    assert "postgres@sha256:" in content, (
        "postgres image is not pinned to a digest"
    )


def test_redis_image_pinned_to_digest():
    """redis image must be pinned to sha256 digest."""
    with open("docker-compose.yml", "r") as f:
        content = f.read()
    assert "redis@sha256:" in content, (
        "redis image is not pinned to a digest"
    )


# ── TEST 3: CSP routing ─────────────────────────────────────────────
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_strict_csp_on_production_routes():
    """Production routes must have strict CSP."""
    response = client.get("/health")
    csp = response.headers.get("content-security-policy", "")
    assert "frame-ancestors 'none'" in csp
    assert "cdn.jsdelivr.net" not in csp


def test_relaxed_csp_on_docs_routes():
    """Docs routes must allow jsdelivr.net."""
    response = client.get("/docs")
    csp = response.headers.get("content-security-policy", "")
    assert "cdn.jsdelivr.net" in csp


def test_openapi_json_has_relaxed_csp():
    """/openapi.json must have relaxed CSP."""
    response = client.get("/openapi.json")
    csp = response.headers.get("content-security-policy", "")
    assert "cdn.jsdelivr.net" in csp