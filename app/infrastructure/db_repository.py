"""
app/infrastructure/db_repository.py
=====================================
Concrete repository implementations using SQLModel and PostgreSQL.

Repository pattern — why it matters:
The repository sits between your domain logic and your database.
Your services never touch the database directly.
They call repository methods — add(), get_by_username(), delete().
This means you can swap PostgreSQL for any other database
without changing a single line of business logic.

This file previously used two separate classes (UserRecord, SessionRecord)
as database models and converted them to domain models (User, SessionModel).
That created 4 tables doing the job of 2.

Fix: User and SessionModel both have table=True — they ARE the database
models. Use them directly. Zero conversion needed. Two tables, not four.
"""

from typing import Optional, List
from sqlmodel import Session as DBSession, select
from app.domain.models import User, SessionModel


# ── USER REPOSITORY ──────────────────────────────────────────────────

class UserRepository:
    """
    Handles all database operations for User objects.

    Why a dedicated repository:
    User operations (create, find by username) are separate concerns
    from session operations. Single responsibility principle.
    Each repository owns one domain object.

    Args:
        db: SQLModel Session — the database connection
            injected via FastAPI's dependency injection
    """

    def __init__(self, db: DBSession):
        # Store the database session
        # All operations use this session
        # Session is created per-request and closed after
        self.db = db

    def add(self, user: User) -> User:
        """
        Creates a new user in the database.
        Checks for duplicates before inserting.

        Args:
            user: User domain object with username, hashed_password, role

        Returns:
            User with id assigned by the database

        Why check for existing first:
        The database has a unique constraint on username.
        Checking first gives a clean return instead of a DB error.
        """
        # Check if username already exists
        existing = self.get_by_username(user.username)
        if existing:
            return existing

        # Add directly — User IS the database model
        # No conversion needed — table=True handles it
        self.db.add(user)
        self.db.commit()

        # refresh() pulls the database-assigned id back into the object
        # Without this, user.id would still be None
        self.db.refresh(user)
        return user

    def get_by_username(self, username: str) -> Optional[User]:
        """
        Finds a user by their username.

        select(User) generates: SELECT * FROM user WHERE username = ?
        .first() returns one result or None — never raises an exception

        Args:
            username: the username to look up

        Returns:
            User if found, None if not found
        """
        return self.db.exec(
            select(User).where(User.username == username)
        ).first()

    def get_all(self) -> List[User]:
        """
        Returns all users in the database.
        Used for admin operations.
        """
        return list(self.db.exec(select(User)).all())


# ── SESSION REPOSITORY ───────────────────────────────────────────────

class SQLSessionRepository:
    """
    Handles all database operations for SessionModel objects.

    SessionModel has table=True so it maps directly to the
    sessionmodel table in PostgreSQL. No intermediate record
    class needed — the domain model IS the database model.

    Args:
        db: SQLModel Session — injected per request
    """

    def __init__(self, db: DBSession):
        self.db = db

    def add(self, session: SessionModel) -> SessionModel:
        """
        Saves a new session to the database.

        Note on computed_field:
        SessionModel.result is a @computed_field — it is calculated
        from greetings * number. It is NOT stored in the database.
        SQLModel knows not to include it in INSERT statements.

        Args:
            session: SessionModel with username, greetings, number, farewell

        Returns:
            SessionModel with database-assigned id
        """
        self.db.add(session)
        self.db.commit()
        self.db.refresh(session)
        return session

    def get_by_username(self, username: str) -> List[SessionModel]:
        """
        Returns all sessions for a specific username.

        SELECT * FROM sessionmodel WHERE username = ?

        Args:
            username: filter sessions by this user

        Returns:
            list of SessionModel objects (empty list if none found)
        """
        return list(
            self.db.exec(
                select(SessionModel).where(SessionModel.username == username)
            ).all()
        )

    def get_all(self) -> List[SessionModel]:
        """
        Returns all sessions in the database.
        Used by admin operations.
        """
        return list(self.db.exec(select(SessionModel)).all())

    def delete(self, session_id: int) -> bool:
        """
        Deletes a session by its ID.

        db.get() is a primary key lookup — fastest possible query
        Returns None if not found — no exception raised

        Args:
            session_id: the primary key of the session to delete

        Returns:
            True if deleted, False if not found
        """
        record = self.db.get(SessionModel, session_id)
        if record is None:
            return False

        self.db.delete(record)
        self.db.commit()
        return True