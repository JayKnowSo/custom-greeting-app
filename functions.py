# functions.py
# Notes: All reusable code lives here
# Functions return values or print messages
# JSON handles persistence
# Main.py only controls flow and menus
# Greeting App helper functions for main.py

import json

# File Names
GREETINGS_LOG_FILE = "greetings_log.json"

def greet(name: str, times: int) -> list[str]:
    return [f"Hello, {name}!" for _ in range(times)]



def farewell(name):
    return f"Goodbye {name}! See you next time!"


def custom_farewell(name, farewell_message):
    return f"{farewell_message}, {name}!"

def load_sessions(filename="greetings_log.json"):
    try:
        with open(filename, "r") as f:
            sessions = json.load(f)

            # Safety check: Json must be on list
            if not isinstance(sessions, list):
                return[]
            
            return sessions
        
    except FileNotFoundError:
        return []
    
def save_sessions(sessions, filename="greetings_log.json"):
    with open(filename, "w") as f:
        json.dump(sessions, f, indent=4)

def save_table_to_file(name, greetings_count, number, farewell_message=None):
    """ Build a multiplication table, saves the session to json, and returns the 
     table for display in main.py
    """
    table = [f"{number} x {i} = {number * i}" for i in range(1, 11)]

    # Build sessions dictionary
    session = {
        "name": name,
        "greetings": greetings_count,
        "farewell": farewell_message or "",
        "multiplication_number": number,
        "multiplication_table": table,
    }

    sessions = load_sessions()
    sessions.append(session)
    save_sessions(sessions)

    return table

# SESSION COUNT PER USER (DICT)
def load_session_counts(filename="Greetings_Log_File"):
    try:
        with open(filename, "r") as f:
            counts = json.load(f)

            if not isinstance(counts, dict):
                return {}

            return counts
    except (FileNotFoundError, json.JSONDecodeError):
        return {}
    
def save_session_counts(counts, filename="Greetings_Log_File"):
    with open(filename, "w") as f:
        json.dump(counts, f, indent=4)

def find_sessions_by_name(sessions: list[dict], name: str) -> list[dict]:
     search_name = name.lower().strip()
     return [s for s in sessions if s["name"].lower() == search_name]

def compute_session_stats(sessions: list[dict]) -> dict:
    """
    Compute summary statistics from session list.
    Returns a dict with total_sessions, total_greetings,
    unique_users, and most_used_number.
    """
    stats = {
        "total_sessions": len(sessions),
        "total_greetings": sum(s["greetings"] for s in sessions),
        "unique_users": len(set(s["name"].lower() for s in sessions)),
        "most_used_number": None,
    }

    if sessions:
        number_counts = {}
        for s in sessions:
            num = s["multiplication_number"]
            number_counts[num] = number_counts.get(num, 0) + 1
        # find the number used most often
        stats["most_used_number"] = max(number_counts, key=number_counts.get)

    return stats
