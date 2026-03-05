# db_repository.py
# This file implements the SQLSessionRepository class,
#  which is a concrete implementation of the SessionRepository interface defined in repositories.py.

from typing import Optional, List
from sqlmodel import Session as DBSession, select
from app.domain.models import User, SessionModel
from app.infrastructure.database import UserRecord, SessionRecord


# -------------------- User Repository --------------------
class UserRepository:
    """Repository for User objects"""

    def __init__(self, db: DBSession):
        self.db = db

    def add(self, user: User) -> User:
        # Check if user already exists to prevent duplicates
        existing = self.get_by_username(user.username)
        if existing:
             return existing
        
        record = UserRecord(
            username=user.username,
            hashed_password=user.hashed_password,
            role=user.role
        )
        self.db.add(record)
        self.db.commit()
        self.db.refresh(record)

        return User(
            id=record.id,
            username=record.username,
            hashed_password=record.hashed_password,
            role=record.role
        )

    def get_by_username(self, username: str) -> Optional[User]:
        record = self.db.exec(select(UserRecord).where(UserRecord.username == username)).first()
        if not record:
            return None

        return User(
            id=record.id,
            username=record.username,
            hashed_password=record.hashed_password,
            role=record.role
        )

    def get_all(self) -> List[User]:
        results = self.db.exec(select(UserRecord)).all()
        return [
            User(
                id=r.id,
                username=r.username,
                hashed_password=r.hashed_password,
                role=r.role
            )
            for r in results
        ]

# -------------------- Session Repository --------------------
class SQLSessionRepository:
    """Repository for Session objects"""

    def __init__(self, db: DBSession):
        self.db = db

    def add(self, session: SessionModel) -> SessionModel:
        record = SessionRecord(
            username=session.username,
            greetings=session.greetings,
            number=session.number,
            farewell=session.farewell
        )
        self.db.add(record)
        self.db.commit()
        self.db.refresh(record)

        return SessionModel(
            id=record.id,
            username=record.username,
            greetings=record.greetings,
            number=record.number,
            farewell=record.farewell
        )

    def get_by_username(self, username: str) -> List[SessionModel]:
        records = self.db.exec(select(SessionRecord).where(SessionRecord.username == username)).all()
        return [
            SessionModel(
                id=r.id,
                username=r.username,
                greetings=r.greetings,
                number=r.number,
                farewell=r.farewell
            )
            for r in records
        ]

    def get_all(self) -> List[SessionModel]:
        results = self.db.exec(select(SessionRecord)).all()
        return [
            SessionModel(
                id=r.id,
                username=r.username,
                greetings=r.greetings,
                number=r.number,
                farewell=r.farewell
            )
            for r in results
        ]

    def delete(self, session_id: int) -> bool:
        record = self.db.get(SessionRecord, session_id)
        if record is None:
            return False

        self.db.delete(record)
        self.db.commit()
        return True
