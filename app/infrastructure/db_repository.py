# db_repository.py
# This file implements the SQLSessionRepository class,
#  which is a concrete implementation of the SessionRepository interface defined in repositories.py.

from typing import List
from sqlmodel import Session as DBSession, select
from app.domain.repositories import SessionRepository
from app.infrastructure.database import SessionRecord, engine
from app.domain.models import SessionModel


class SQLSessionRepository(SessionRepository):
    def __init__(self, db: DBSession):
        """
        Initializes the repository with a database session.
        """
        self.db = db

    def add(self, session: SessionModel) -> SessionModel:
        """
        Adds a new session to the database and returns the inserted session as a SessionModel.
        """
        try:
            record = SessionRecord(
                name=session.name,
                greetings=session.greetings,
                number=session.number,
                farewell=session.farewell
            )
            self.db.add(record)
            self.db.commit()
            self.db.refresh(record)

            return SessionModel(
                id=record.id,
                name=record.name,
                greetings=record.greetings,
                number=record.number,
                farewell=record.farewell
            )
        except Exception as e:
            self.db.rollback()  # Rollback in case of any error
            raise e  # Re-raise the error after logging it

    def get_by_username(self, username: str) -> List[SessionModel]:
        """
        Retrieves sessions that match the given username.
        """
        statement = select(SessionRecord).where(SessionRecord.name.ilike(f"%{username}%"))
        records = self.db.exec(statement).all()

        return [
            SessionModel(
                id=r.id,
                name=r.name,
                greetings=r.greetings,
                number=r.number,
                farewell=r.farewell
            )
            for r in records
        ]

    def get_all(self) -> List[SessionModel]:
        """
        Retrieves all sessions from the database.
        """
        results = self.db.exec(select(SessionRecord)).all()
        
        return [
            SessionModel(
                id=r.id,
                name=r.name,
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


