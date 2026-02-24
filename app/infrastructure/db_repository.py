# db_repository.py
# This file implements the SQLSessionRepository class,
#  which is a concrete implementation of the SessionRepository interface defined in repositories.py.

from sqlmodel import Session, select
from app.domain.models import SessionModel
from app.domain.repositories import SessionRepository

class SQLSessionRepository(SessionRepository):
    def __init__(self, db: Session):
        self.db = db

    def add(self, session: SessionModel) -> SessionModel:
        self.db.add(session)
        self.db.commit()
        self.db.refresh(session)
        return session

    def get_by_username(self, username: str):
        statement = select(SessionModel).where(SessionModel.name == username)
        return self.db.exec(statement).all()

    def get_all(self):
        statement = select(SessionModel)
        return self.db.exec(statement).all()


