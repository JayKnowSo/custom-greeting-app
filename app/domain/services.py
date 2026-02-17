from app.infrastructure.functions  import SessionModel, save_table_to_file, load_sessions
from app.infrastructure.database import SessionRecord, engine
from sqlmodel import Session as DBSession, select
from typing import List


# Domain services for the Greeting App
# Services contain business logic and coordinate between infrastructure functions and API routes. They can also include additional logic for validation, data transformation, or complex operations that involve multiple steps.

def save_session_to_db(name: str, greetings: int, number: int, farewell: str):
    """
    Save a session to the SQLite DB using infrastructure function
    """
    return save_table_to_file(name, greetings, number, farewell, use_db=True)

# Function to retrieve all sessions from the SQLite DB using SQLModel
def get_all_sessions_from_db() -> List[SessionRecord]:
    """ Retrieve all sessions from the SQLite DB using SQLModel"""
    with DBSession(engine) as db:
        return db.exec(select(SessionRecord)).all()


def compute_db_stats(db: DBSession) -> dict:
    sessions = db.exec(select(SessionRecord)).all()

    stats = {
        "total_sessions": len(sessions),
        "total_greetings": sum(s.greetings for s in sessions),
        "unique_users": len(set(s.name.lower() for s in sessions)),
        "most_used_number": None,
    }

    if sessions:
        counts = {}
        for s in sessions:
            counts[s.multiplication_number] = counts.get(s.multiplication_number, 0) + 1
        stats["most_used_number"] = max(counts, key=counts.get)

    return stats

# Function to search sessions by name using SQLModel
def search_sessions_by_name(db, name: str):
    statement = select(SessionRecord).where(
        SessionRecord.name.ilike(f"%{name}%")
    )

    results = db.exec(statement).all()

    return [
        {
            "name": s.name,
            "greetings": s.greetings,
            "number": s.multiplication_number,
            "farewell": s.farewell
        }
        for s in results
    ]
