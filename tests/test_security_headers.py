# tests/test_security_headers.py
from fastapi.testclient import TestClient
from app.main import app

# This test file checks that the security headers are present on every response from the API,
# and that they have the correct values. It also checks that the Server header is removed 
# to prevent fingerprinting of the server stack. The tests ensure that the security
# headers are included on both successful

client = TestClient(app)

# The test_security_headers_present_on_every_response function checks 
# that all the expected security headers are present in the response from the root endpoint.
# The test_hsts_value_is_correct function verifies that the Strict-Transport-Security 
# header is set to enforce HTTPS for at least one year.

def test_security_headers_present_on_every_response():
    """Every response must carry all security headers."""
    response = client.get("/")
    
    assert "strict-transport-security" in response.headers
    assert "x-content-type-options" in response.headers
    assert "x-frame-options" in response.headers
    assert "content-security-policy" in response.headers
    assert "referrer-policy" in response.headers
    assert "permissions-policy" in response.headers

# The test_no_clickjacking function checks that the X-Frame-Options header is set to DENY,
# which prevents the page from being embedded in iframes and protects against clickjacking attacks.
# The test_no_mime_sniffing function verifies that the X-Content-Type-Options header 
# is set to nosniff, which prevents MIME sniffing and ensures that the browser respects the declared content type.
# The test_csp_blocks_external_sources function checks that the Content-Security-Policy header
# restricts sources to self only, which helps to block injected scripts and other malicious content.
# The test_server_header_removed function verifies that the Server header is removed from the response,
# which helps to prevent fingerprinting of the server stack and reduces the attack surface.
# The test_headers_present_on_error_responses function ensures that the security headers are included
# on error responses as well, not just on successful responses.

def test_hsts_value_is_correct():
    """HSTS must enforce HTTPS for at least 1 year."""
    response = client.get("/")
    hsts = response.headers["strict-transport-security"]
    assert "max-age=31536000" in hsts
    assert "includeSubDomains" in hsts


def test_no_clickjacking():
    """X-Frame-Options must be DENY — no iframes allowed."""
    response = client.get("/")
    assert response.headers["x-frame-options"] == "DENY"


def test_no_mime_sniffing():
    """Browser must not guess content type."""
    response = client.get("/")
    assert response.headers["x-content-type-options"] == "nosniff"


def test_csp_blocks_external_sources():
    """CSP must restrict sources to self only."""
    response = client.get("/")
    csp = response.headers["content-security-policy"]
    assert "default-src 'self'" in csp
    assert "frame-ancestors 'none'" in csp


def test_server_header_removed():
    """Server fingerprint must be removed — don't advertise your stack."""
    response = client.get("/")
    assert "server" not in response.headers


def test_headers_present_on_error_responses():
    """Security headers must appear on error responses too — not just 200s."""
    response = client.get("/nonexistent-route")
    assert "x-content-type-options" in response.headers
    assert "x-frame-options" in response.headers