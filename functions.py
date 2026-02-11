# functions.py
# Notes: All reusable code lives here
# Functions return values or print messages
# JSON handles persistence
# Main.py only controls flow and menus

import json
import os

# File Names
GREETINGS_LOG_FILE = "greetings_log.json"
SESSION_COUNT_FILE = "session_counts.json"

def greet(name, times):
    return [f"Hello, {name}!" for _ in range(times)]



def farewell(name):
    print(f"Goodbye {name}! See you next time!")


def custom_farewell(name, farewell_message):
    print(f"{farewell_message}, {name}!")

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
def load_session_counts(filename=SESSION_COUNT_FILE):
    try:
        with open(filename, "r") as f:
            counts = json.load(f)

            if not isinstance(counts, dict):
                return {}

            return counts
    except FileNotFoundError:
        return {}
    
def parse_greetings_log(filename=GREETINGS_LOG_FILE):
    """
    Parse the greetings log into a clean list of session dictionaries.
    """
    sessions = load_sessions(filename)

    parsed = []
    for session in sessions:
        parsed.append({
            "name": session.get("name", ""),
            "greetings": session.get("greetings", 0),
            "multiplication_number": session.get("multiplication_number", 0),
            "multiplication_table": session.get("multiplication_table", []),
            "farewell": session.get("farewell", "")
        })

    return parsed



def save_session_counts(counts, filename=SESSION_COUNT_FILE):
    with open(filename, "w") as f:
        json.dump(counts, f, indent=4)


def increment_user_session(name):
    counts = load_session_counts()

    if name in counts:
        counts[name] += 1
    else:
        counts[name] = 1

    save_session_counts(counts)
    return counts[name]


def display_session_counts():
    counts = load_session_counts()

    if not counts:
        print("\nNo session counts recorded yet.")
        return

    print("\n--- Session Count Per User ---")
    for name, count in counts.items():
        print(f"{name}: {count}")

   # Session Queries
def list_user_names(sessions):
    return sorted(set(session["name"] for session in sessions))

def find_sessions_by_name(sessions, name):
     search_name = name.lower().strip()
     return [s for s in sessions if s["name"].lower() == search_name]