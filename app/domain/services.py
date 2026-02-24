from app.domain.models import SessionModel, SessionCreate
from app.domain.repositories import SessionRepository


class GreetingService:

    def __init__(self, repository: SessionRepository):
        self.repository = repository

    def create_session(self, name: str, greetings: int, number: int, farewell: str) -> SessionModel:
        record = SessionModel(
            name=name,
            greetings=greetings,
            number=number,
            farewell=farewell
        )
        return self.repository.add(record)

    def search_sessions(self, username: str) -> list[SessionModel]:
        return self.repository.get_by_username(username)

    def get_sessions(self) -> list[SessionModel]:
        return self.repository.get_all()

    def get_stats(self) -> dict:
        sessions = self.get_sessions()

        stats = {
            "total_sessions": len(sessions),
            "total_greetings": sum(s.greetings for s in sessions),
            "unique_users": len(set(s.name.lower() for s in sessions)),
            "most_used_number": None,
        }

        if sessions:
            counts = {}
            for s in sessions:
                counts[s.number] = counts.get(s.number, 0) + 1

            stats["most_used_number"] = max(counts, key=counts.get)

        return stats