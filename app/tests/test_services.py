from app.domain.services import GreetingService
from app.infrastructure.db_repository import SQLSessionRepository
from app.infrastructure.database import engine
from sqlmodel import Session
from app.domain.models import SessionModel


def test_create_and_read_session_db():

    with Session(engine) as db:

        repo = SQLSessionRepository(db)

        service = GreetingService(repo)

        session = SessionModel(
            name="TestUser",
            greetings=3,
            number=5,
            farewell="bye"
        )

        service.create_session(session)

        sessions = service.get_sessions()

        assert len(sessions) > 0

def test_delete_session_db():

    with Session(engine) as db:

        repo = SQLSessionRepository(db)

        service = GreetingService(repo)

        session = SessionModel(
            name="DeleteUser",
            greetings=1,
            number=2,
            farewell="bye"
        )

        created = service.create_session(session)

        deleted = service.delete_session(created.id)

        assert deleted is True  
