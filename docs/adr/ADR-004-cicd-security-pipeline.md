# ADR-004: CI/CD Security Pipeline — GitHub Actions

**Date:** 2026-03-17  
**Status:** Accepted  
**Author:** Jemel Padilla

## Context

Phase 1 established a hardened Docker stack with documented CVE 
findings and 53 passing security tests. All validation was manual —
tests were run locally, Trivy scans were run on demand, and results
were committed manually.

Manual security validation has three critical failure modes:

1. Human error — a developer forgets to run tests before pushing
2. Inconsistency — different developers run different checks
3. No gate — bad code can reach the main branch unchallenged

A CI/CD security pipeline eliminates all three failure modes by
automating security validation on every push.

## Decision

Implement a two-job GitHub Actions pipeline triggered on every
push and pull request to main:

**Job 1: Security Tests**
- Runs on ubuntu-latest (fresh VM every run)
- Sets up Python 3.12 (matches Dockerfile)
- Installs dependencies from requirements.txt
- Runs full 53-test suite with DATABASE_URL override
- Fails pipeline if any test fails

**Job 2: Container CVE Scan (depends on Job 1)**
- Builds Docker image from Dockerfile
- Runs Trivy scan using aquasecurity/trivy-action
- Fails pipeline on CRITICAL CVEs with available fixes
- ignore-unfixed: true matches ADR-002 accepted risk decision
- Uploads scan results as artifact (30-day retention)
- Only runs if Job 1 passes — no point scanning broken code

## Consequences

**Positive:**
- Every push to main is automatically validated
- Bad code cannot reach production silently
- CRITICAL CVEs with available fixes are caught before deployment
- Test results and scan artifacts are stored per run
- Pipeline enforces the same security standard as local development
- Shift-left security — problems caught at commit time cost 
  10x less to fix than problems caught in production
- Public GitHub Actions badge signals security maturity to recruiters

**Negative:**
- Pipeline adds ~3 minutes to every push
- Docker build in CI is slower than local (no layer cache)
- Trivy database must be downloaded on every run

## Alternatives Considered

- **No CI/CD**: rejected — manual validation is unreliable at scale
- **CircleCI**: considered — GitHub Actions chosen for native 
  integration, no additional account required, free for public repos
- **Jenkins**: rejected — requires self-hosted server, 
  significant operational overhead for a solo project
- **GitLab CI**: rejected — would require migrating repository
- **Pre-commit hooks only**: rejected — hooks run locally and can 
  be bypassed with --no-verify. Pipeline cannot be bypassed.

## Implementation Notes

Pipeline file: .github/workflows/security.yml

Key design decisions:
- needs: test on trivy job ensures sequential execution
- exit-code: 1 on Trivy makes the scan a hard gate
- ignore-unfixed: true is consistent with ADR-002
- DATABASE_URL injected as env var — same pattern as pytest.ini
- SECRET_KEY uses a test value — never real secrets in CI

## Security Relevance

A CI/CD pipeline is not just an automation tool. It is a security
control. It enforces the security standard on every contribution,
from every developer, on every push — without relying on human
memory or discipline.

This is the foundation of DevSecOps: security as code,
automated, non-negotiable, and auditable.

The pipeline is public. Every run is logged. Every result is
stored. This is security posture as a public artifact.

## Career Relevance

Every Cloud Security Engineer and DevSecOps role at the
senior level requires CI/CD pipeline experience. This ADR
documents not just what was built but why — the tradeoffs
considered, the alternatives rejected, and the security
principles applied.

In an interview, this ADR answers:
- "Have you built a CI/CD pipeline?"
- "How do you handle security in your pipeline?"
- "What is shift-left security?"
- "Why GitHub Actions over Jenkins?"

All four questions. One document.
