from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

# The headers.py file defines a middleware class that adds security headers to all HTTP responses.
# The SecurityHeadersMiddleware class inherits from BaseHTTPMiddleware 
# and overrides the dispatch method to add various security headers to the response.
# The headers added include Strict-Transport-Security, X-Content-Type-Options,
#  X-Frame-Options, X-XSS-Protection, Content-Security-Policy, Referrer-Policy, and Permissions-Policy.
# Additionally, the middleware removes any Server

DOCS_PATHS = {"/docs", "/redoc", "/openapi.json"} # Set of paths that serve API documentation,
                                                  # which may require a more relaxed Content Security Policy 
                                                  # CSP to allow loading external resources like stylesheets and scripts from CDNs.

DOCS_CSP = (
    "default-src 'self'; "
    "script-src 'self' https://cdn.jsdelivr.net 'unsafe-inline'; " # Allow scripts from the same origin and from the jsDelivr CDN, 
                                                                    # and allow inline scripts for documentation pages.
    "style-src 'self' https://cdn.jsdelivr.net 'unsafe-inline'; "    # Allow styles from the same origin and from the jsDelivr CDN,
                                                                    # and allow inline styles for documentation pages.
    "img-src 'self' https://fastapi.tiangolo.com data:; "
    "connect-src 'self'"
)

STRICT_CSP = (
    "default-src 'self'; "
    "script-src 'self'; "
    "style-src 'self'; "
    "img-src 'self'; "
    "connect-src 'self'; "
    "frame-ancestors 'none'"
)


class SecurityHeadersMiddleware(BaseHTTPMiddleware):

      async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        is_docs = request.url.path in DOCS_PATHS
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Content-Security-Policy"] = DOCS_CSP if is_docs else STRICT_CSP
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Permissions-Policy"] = "geolocation=(), microphone=(), camera=(), payment=(), usb=()"
        if "server" in response.headers:
            del response.headers["server"]
        if "x-powered-by" in response.headers:
            del response.headers["x-powered-by"]
        return response
