# functions.py
# Notes: All reusable code lives here
# Functions return values or print messages
import re

def greet(name, times):
    for i in range(times):
        print(f"Hello {name}! (greeting {i+1})")


def farewell(name):
    print(f"Goodbye {name}! See you next time!")


def custom_farewell(name, farewell_message):
    print(f"{farewell_message}, {name}!")


def save_table_to_file(name, number, table):
    """Saves the multiplication table to a log file."""
    with open("greetings_log.txt", "a") as file:
        file.write(f"{name}'s multiplication table for {number}:\n")
        for line in table:
            file.write(line + "\n")
        file.write("-" * 30 + "\n")


def read_greetings_log():
    """Reads and returns the contents of greetings_log.txt."""
    try:
        with open("greetings_log.txt", "r") as file:
            return file.read()
    except FileNotFoundError:
        return "The greetings log file does not exist yet."


def parse_greetings_log():
    """Parse greetings_log.txt into structured data."""
    sessions = []
    current_session = None
    header_re = re.compile(r"^(?P<name>.+?)'s multiplication table for (?P<number>\d+):$")

    try:
        with open("greetings_log.txt", "r") as file:
            for line in file:
                line = line.strip()

                if not line:
                    continue  # Skip empty lines

                if line.startswith("-"):
                    if current_session:
                        sessions.append(current_session)
                        current_session = None
                    continue

                # Header lines like "Alice's multiplication table for 5:"
                m = header_re.match(line)
                if m:
                    name = m.group("name")
                    number = int(m.group("number"))
                    current_session = {"name": name, "multiplication_number": number, "table": []}
                    continue

                # Table entry lines, e.g. "5 x 1 = 5"
                if " x " in line and current_session:
                    current_session["table"].append(line)
                    continue

                # Fallback: if we encounter an unexpected line, start a session with raw name
                if not current_session:
                    current_session = {"name": line, "multiplication_number": None, "table": []}

        if current_session:
            sessions.append(current_session)
    except FileNotFoundError:
        pass

    return sessions


def count_sessions(sessions):
    """Counts total number of sessions in the log."""
    return len(sessions)


def list_user_names(sessions):
    """Return a list of all user names from the sessions."""
    names = set()
    for session in sessions:
        names.add(session["name"])
    return list(names)