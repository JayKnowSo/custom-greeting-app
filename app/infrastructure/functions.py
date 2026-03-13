# functions.py
# Notes: All reusable code lives here
# Functions return values or print messages
# JSON handles persistence
# Main.py only controls flow and menus
# Greeting App helper functions for main.py

import json
from pydantic import ValidationError
from app.infrastructure.database import SessionRecord, engine
from sqlmodel import Session as DBSession


# File Names
GREETINGS_LOG_FILE = "greetings_log.json"


# Your helper functions go here
def greet(name: str, times: int) -> list[str]:
    return [f"Hello, {name}!" for _ in range(times)]

def farewell(name: str) -> str:
    return f"Goodbye {name}! See you next time!"


def custom_farewell(name, farewell_message):
    return f"{farewell_message}, {name}!"

def load_sessions(filename="greetings_log.json"):
    try:
        with open(filename, "r") as f:
            sessions = json.load(f)

            # Safety check: Json must be on list
            if not isinstance(sessions, list):
                return []

            return sessions

    except FileNotFoundError:
        return []

def save_sessions(sessions, filename="greetings_log.json"):
    with open(filename, "w") as f:
        json.dump(sessions, f, indent=4)

def save_table_to_file(name: str, greetings_count: int, number: int, farewell_message: str = None, use_db: bool = False):
    # ensure numeric types before building SQL/Model to avoid SQLAlchemy emitting DB-specific casts
    try:
        greetings_count = int(greetings_count)
        number = int(number)
    except (TypeError, ValueError):
        print("greetings_count and number must be integers")
        return []

    table = [f"{number} x {i} = {number * i}" for i in range(1, 11)]
    """
    Build multiplication table and save session.
    If use_db=True, save to SQLite DB; otherwise save to JSON.
    """
    # Build session using Pydantic/SQLModel model
    try:
        session = SessionRecord(
            username=name,
            greetings=greetings_count,
            number=number,
            farewell=farewell_message or ""
        )
    except ValidationError as e:
        print("Session data is invalid:", e)
        return []

    if use_db:
        # add the validated model instance directly; types are already native Python types
        with DBSession(engine) as db:
            db.add(session)
            db.commit()
            db.refresh(session)
    else:
        sessions = load_sessions()
        sessions.append(session.model_dump())
        save_sessions(sessions)

    return table

def save_session_counts(counts, filename="greetings_log.json"):
    with open(filename, "w") as f:
        json.dump(counts, f, indent=4)

def find_sessions_by_name(sessions: list[dict], name: str) -> list[dict]:
    search_name = name.lower().strip()
    return [s for s in sessions if s.get("username", "").lower() == search_name.lower()]
# ...existing code...
def compute_session_stats(sessions: list[dict]) -> dict:
    """
    Compute summary statistics from session list.
    Returns a dict with total_sessions, total_greetings,
    unique_users, and most_used_number.
    """
    stats = {
        "total_sessions": len(sessions),
        "total_greetings": sum(int(s.get("greetings", 0)) for s in sessions),
        "unique_users": len(set(s.get("name", "").lower() for s in sessions)),
        "most_used_number": None,
    }

    if sessions:
        number_counts = {}
        for s in sessions:
            num = int(s.get("number", 0))
            number_counts[num] = number_counts.get(num, 0) + 1
        # find the number used most often
        stats["most_used_number"] = max(number_counts, key=number_counts.get)

    return stats
