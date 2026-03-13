# ── STAGE 1: BUILDER ──────────────────────────────────────────────
# Install dependencies in a separate stage
# This keeps the final image clean and small
FROM python:3.12-slim AS builder

WORKDIR /build

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first — Docker caches this layer
# Only rebuilds when requirements.txt changes
COPY requirements.txt .

# Install all dependencies into a local folder
RUN pip install --upgrade pip && \
    pip install --prefix=/install --no-cache-dir -r requirements.txt


# ── STAGE 2: RUNTIME ──────────────────────────────────────────────
# Final image — only what's needed to run the app
FROM python:3.12-slim AS runtime

WORKDIR /app

# Install only runtime system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    && rm -rf /var/lib/apt/lists/*

# Copy installed Python packages from builder stage
COPY --from=builder /install /usr/local

# Create a non-root user — never run as root in production
# If an attacker exploits the app they get this user, not root
RUN groupadd --gid 1001 appgroup && \
    useradd --uid 1001 --gid appgroup --no-create-home appuser

# Copy application code
COPY app/ ./app/

# Change ownership to non-root user
RUN chown -R appuser:appgroup /app

# Switch to non-root user
USER appuser

# Expose the port FastAPI runs on
EXPOSE 8000

# Health check — Docker will monitor this
# If /health returns non-200, container is marked unhealthy
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD python -c "import httpx; httpx.get('http://localhost:8000/health').raise_for_status()"

# Start the app
# --host 0.0.0.0 makes it accessible outside the container
# --workers 1 for now — scale in AWS later
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
