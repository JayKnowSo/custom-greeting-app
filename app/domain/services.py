


from typing import List
from app.domain.models import SessionModel
from app.infrastructure.db_repository import SQLSessionRepository

class GreetingService:
    """
    Business logic layer.

    Depends only on the repository interface,
    not on database implementations.
    """

    def __init__(self, repository: SQLSessionRepository):
        self.repository = repository

    # -------------------- Create greeting --------------------
    def create_greeting(self, session: SessionModel) -> SessionModel:
        created = self.repository.add(session)

        # DEBUG: check what is returned
        print("Created session type:", type(created))
        print("Created session value:", created)

        return created

    # -------------------- Search / List --------------------
    def search_sessions(self, username: str) -> List[SessionModel]:
        return self.repository.get_by_username(username)

    def get_sessions(self) -> List[SessionModel]:
        return self.repository.get_all()

    # -------------------- Delete --------------------
    def delete_session(self, session_id: int) -> bool:
        return self.repository.delete(session_id)

    # -------------------- Stats --------------------
    def get_stats(self) -> dict:
        sessions = self.repository.get_all()
        stats = {
            "total_sessions": len(sessions),
            "total_greetings": sum(s.greetings for s in sessions),
            "unique_users": len(set(s.username.lower() for s in sessions)),
            "most_used_number": None,
        }

        if sessions:
            counts = {}
            for s in sessions:
                counts[s.number] = counts.get(s.number, 0) + 1
            stats["most_used_number"] = max(counts, key=counts.get)

        return stats