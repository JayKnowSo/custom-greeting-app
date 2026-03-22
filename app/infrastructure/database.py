"""
app/infrastructure/database.py
================================
Database connection and engine setup.

This file has one job:
Create the database engine and provide the session dependency.

What was removed:
SessionRecord and UserRecord were duplicate table definitions.
They duplicated SessionModel and User from app/domain/models.py
causing 4 tables in PostgreSQL instead of 2.

Single source of truth:
app/domain/models.py owns ALL table definitions.
This file owns ONLY the connection.

Architecture principle:
Infrastructure layer handles HOW we connect.
Domain layer handles WHAT we store.
Never mix the two.
"""

import os
from dotenv import load_dotenv
from sqlmodel import SQLModel, create_engine, Session

# load_dotenv() reads .env file into environment variables
# Must be called before os.getenv() or the values won't be available
# In Docker: docker-compose.yml injects env vars directly
# Locally: .env file provides them
load_dotenv()

# DATABASE_URL controls which database engine to use
# PostgreSQL: postgresql+psycopg://user:pass@host:port/dbname
# SQLite:     sqlite:///./filename.db (local testing only)
# Default fallback to SQLite prevents crashes during local development
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test_local.db")

# Log which database we're connecting to
# Helps debug environment mismatches immediately
print("DATABASE_URL =", DATABASE_URL)

# Create engine based on database type
# SQLite needs check_same_thread=False for FastAPI's async handling
# PostgreSQL needs pool_pre_ping=True to detect stale connections
if "sqlite" in DATABASE_URL:
    engine = create_engine(
        DATABASE_URL,
        echo=True,                                  # logs all SQL queries
        connect_args={"check_same_thread": False}   # required for SQLite + FastAPI
    )
else:
    engine = create_engine(
        DATABASE_URL,
        echo=True,          # logs all SQL queries — disable in production
        pool_pre_ping=True  # tests connection before using from pool
                            # prevents errors from stale/dropped connections
    )


def create_db() -> None:
    """
    Creates all database tables defined in domain models.

    SQLModel.metadata.create_all() scans all classes with table=True
    and creates their tables if they don't exist.

    Called once on application startup via the lifespan function in main.py.
    Safe to call multiple times — won't recreate existing tables.

    Tables created:
        user         ← from app.domain.models.User
        sessionmodel ← from app.domain.models.SessionModel
    """
    SQLModel.metadata.create_all(engine)


def get_db():
    """
    FastAPI dependency that provides a database session per request.

    yield creates a context manager:
    → Session opens when request starts
    → Code runs with the session
    → Session closes automatically when request ends
      (even if an exception occurs)

    Usage in routes:
        db: Session = Depends(get_db)

    Why per-request sessions:
    Database connections are expensive.
    Opening one per request and closing it immediately
    prevents connection leaks and pool exhaustion.
    """
    with Session(engine) as session:
        yield session



