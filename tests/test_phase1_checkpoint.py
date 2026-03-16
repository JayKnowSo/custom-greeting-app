"""
Phase 1 TDD Checkpoint
Proves every security decision made in Phase 1 actually works.
These tests must pass before Phase 1 can be closed.
"""
import subprocess
import yaml
import pytest
from fastapi.testclient import TestClient
from app.main import app


# ── TEST 1: pip CVE remediation ────────────────────────────────────
# Proves pip was upgraded in the runtime stage of the Docker image.
# CVE-2025-8869 and CVE-2026-1703 are fixed in pip 25.3 and 26.0.
# This test confirms the running container has pip >= 25.3.

def test_pip_version_remediated_in_runtime():
    """pip inside the container must be >= 25.3 to clear CVE-2025-8869."""
    result = subprocess.run(
        ["docker", "exec", "greeting_app", "pip", "--version"],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, "Could not exec into container"
    output = result.stdout
    # Extract version number from "pip X.Y.Z from ..."
    version_str = output.split()[1]
    major, minor = int(version_str.split(".")[0]), int(version_str.split(".")[1])
    assert (major, minor) >= (25, 3), (
        f"pip {version_str} is vulnerable. Must be >= 25.3 to clear CVE-2025-8869"
    )


# ── TEST 2: Image digest pinning ───────────────────────────────────
# Proves docker-compose.yml references images by sha256 digest.
# Floating tags like postgres:16-alpine can change without warning.
# Digest pinning ensures supply chain integrity.

def test_postgres_image_pinned_to_digest():
    """postgres image must be pinned to sha256 digest not a floating tag."""
    with open("docker-compose.yml", "r") as f:
        compose = yaml.safe_load(f)
    postgres_image = compose["services"]["db"]["image"]
    assert "sha256:" in postgres_image, (
        f"postgres image '{postgres_image}' is not pinned to a digest. "
        "Use image: postgres@sha256:... for supply chain integrity."
    )


def test_redis_image_pinned_to_digest():
    """redis image must be pinned to sha256 digest not a floating tag."""
    with open("docker-compose.yml", "r") as f:
        compose = yaml.safe_load(f)
    redis_image = compose["services"]["redis"]["image"]
    assert "sha256:" in redis_image, (
        f"redis image '{redis_image}' is not pinned to a digest. "
        "Use image: redis@sha256:... for supply chain integrity."
    )


# ── TEST 3: CSP routing ────────────────────────────────────────────
# Proves strict CSP is applied on production routes
# and relaxed CSP is only applied on docs routes.
# This is the security principle of least privilege applied to headers.

client = TestClient(app)


def test_strict_csp_on_production_routes():
    """Production routes must have strict CSP — no external sources allowed."""
    response = client.get("/health")
    csp = response.headers.get("content-security-policy", "")
    assert "frame-ancestors 'none'" in csp, (
        "Production routes must include frame-ancestors 'none' in CSP"
    )
    assert "cdn.jsdelivr.net" not in csp, (
        "Production routes must NOT allow cdn.jsdelivr.net in CSP"
    )


def test_relaxed_csp_on_docs_routes():
    """Docs routes must allow jsdelivr.net for Swagger UI to load."""
    response = client.get("/docs")
    csp = response.headers.get("content-security-policy", "")
    assert "cdn.jsdelivr.net" in csp, (
        "Docs routes must allow cdn.jsdelivr.net for Swagger UI"
    )


def test_strict_csp_on_root():
    """Root endpoint must have strict CSP."""
    response = client.get("/")
    csp = response.headers.get("content-security-policy", "")
    assert "cdn.jsdelivr.net" not in csp, (
        "Root endpoint must not allow external CDN sources"
    )


def test_openapi_json_has_relaxed_csp():
    """/openapi.json is a docs route and must have relaxed CSP."""
    response = client.get("/openapi.json")
    csp = response.headers.get("content-security-policy", "")
    assert "cdn.jsdelivr.net" in csp, (
        "/openapi.json must allow jsdelivr.net — it serves the API schema"
    )
