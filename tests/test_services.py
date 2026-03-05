from app.domain.services import GreetingService
from app.infrastructure.db_repository import SQLSessionRepository
from app.domain.models import SessionModel


def test_create_and_read_session_db(session):

        repo = SQLSessionRepository(session)

        service = GreetingService(repo)

        session_model = SessionModel(
            username="TestUser",
            greetings=3,
            number=5,
            farewell="bye"
        )

        service.create_greeting(session_model)

        sessions = service.get_sessions()

        assert len(sessions) > 0

def test_delete_session_db(session):

        repo = SQLSessionRepository(session)

        service = GreetingService(repo)

        session_model = SessionModel(
            username="DeleteUser",
            greetings=1,
            number=2,
            farewell="bye"
        )

        created = service.create_greeting(session_model)

        deleted = service.delete_session(created.id)

        assert deleted is True  
