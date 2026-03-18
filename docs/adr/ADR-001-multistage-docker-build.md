# ADR-001: Multi-Stage Docker Build

**Date:** 2026-03-13  
**Status:** Accepted  
**Author:** Jemel Padilla

## Context

The application requires PostgreSQL connectivity (psycopg2) which must be
compiled from source. Compilation requires gcc and libpq-dev — build tools
that are not needed at runtime. A single-stage build would include these
tools in the production image, increasing attack surface and image size.

## Decision

Use a multi-stage Dockerfile with two stages:

- **builder**: installs gcc, libpq-dev, compiles all Python dependencies
- **runtime**: copies only compiled packages, installs libpq5 (runtime only)

## Consequences

**Positive:**
- Production image contains zero build tools
- libpq-dev (~30MB) replaced with libpq5 (~500KB) in runtime
- Reduced CVE exposure — fewer packages = fewer vulnerabilities
- Non-root user (appuser UID 1001) runs the application
- Image passes Trivy scan with zero CRITICAL CVEs

**Negative:**
- Slightly longer build time (two stages vs one)
- More complex Dockerfile to maintain

## Alternatives Considered

- **Single-stage build**: rejected — ships gcc and build headers to production
- **Alpine Python base**: considered — further reduces size but psycopg2
  compilation on Alpine requires additional workarounds

## Security Relevance

Every package in a production image is an attack surface. Multi-stage builds
enforce the principle of least privilege at the image layer — the runtime
environment contains only what is needed to run the application.
