from app.domain.models  import SessionModel 
from app.infrastructure.functions import save_table_to_file
from app.infrastructure.database import SessionRecord, engine
from app.domain.repositories import SessionRepository
from typing import List

class GreetingService:

    def __init__(self, repository: SessionRepository):
        self.repository = repository

    
    
    def create_session(self, data: SessionModel):
        return self.repository.add(data)
    
    
    
    def serch_sessions(self, username: str):
        return self.repository.get_by_username(username)

    
    
    def get_stats(self):
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
                counts[s.multiplication_number] = counts.get(
                    s.multiplication_number, 0
                ) + 1

            stats["most_used_number"] = max(counts, key=counts.get)
            return stats
    
