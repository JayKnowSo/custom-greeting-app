# db_repository.py
# This file implements the SQLSessionRepository class,
#  which is a concrete implementation of the SessionRepository interface defined in repositories.py.


from typing import List
from app.domain.models import SessionModel
from app.domain.repositories import SessionRepository
from app.infrastructure.database import SessionRecord, engine
from sqlmodel import Session as DBSession, select


class SQLSessionRepository(SessionRepository):
    def add(self, session: SessionModel):

        record = SessionRecord(
            name=session.name,
            greetings=session.greetings,
            number=session.number,
            farewell=session.farewell,
        )

        with DBSession(engine) as db:
            db.add(record)
            db.commit()
            db.refresh(record)
        return record
    

    def get_by_username(self, username: str) -> List[SessionModel]:
        with DBSession(engine) as db:
            statement = select(SessionRecord).where(SessionRecord.name.ilike(username)
            )
            results = db.exec(statement).all()
            return results
        

    def get_all_sessions(self) -> List[SessionModel]:
        with DBSession(engine) as db:
            return db.exec(select(SessionRecord)).all()


