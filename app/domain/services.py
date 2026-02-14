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
        results = db.exec(select(SessionRecord)).all()
        return results