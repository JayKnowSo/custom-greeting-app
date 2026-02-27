from app.domain.models import SessionModel
from app.domain.repositories import SessionRepository
from typing import List


class GreetingService:

    def __init__(self, repository: SessionRepository):
        self.repository = repository


    def create_session(self, data: SessionModel) -> SessionModel:
        return self.repository.add(data)


    def search_sessions(self, username: str) -> List[SessionModel]:
        return self.repository.get_by_username(username)


    def get_sessions(self) -> List[SessionModel]:
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