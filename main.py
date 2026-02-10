"""Main runner for the Custom Greeting App.

This module coordinates user interaction and uses helper functions
from the project to generate greetings and multiplication tables.
"""

from functions import (
    greet,
    custom_farewell,
    load_sessions,
    save_table_to_file,
    parse_greetings_log,
    list_user_names,
    find_sessions_by_name,
    increment_user_session,
    display_session_counts,
    
)
from helpers import get_nonempty_name, get_positive_number, get_yes_no

# --- Debug Helper ---
DEBUG = False  # Set True to see debug messages

def debug(msg):
    """Print debug messages only if DEBUG is True."""
    if DEBUG:
        print(f"[DEBUG] {msg}")

# --- Helper Function To Display Parsed Sessions ---
def display_parsed_sessions(sessions):
    """Print all session entries in a readable format:
       - Name
       - Greetings count
       - Multiplication number
       - Multiplication table
       - Farewell message (if any)"""
    for session in sessions:
        name = session.get("name")
        greetings = session.get("greetings")
        number = session.get("multiplication_number", 0)
        table = session.get("multiplication_table", [])
        farewell_message = session.get("farewell", "")

        print("\n--- Session ---")
        print(f"Name: {name}")
        print(f"Greetings: {greetings}")
        print(f"Multiplication Number: {number}")

        print(f"\nMultiplication Table for {name}:")
        for line in table:
            print(" ", line)
            if farewell_message: 
                print(f"\nFarewell Message: {farewell_message}")

def show_menu():
    print("\n=== Greeting App Menu ===")
    print("A) Start a greeting session")
    print("B) View session count per user")
    print("C) Exit")

def run_greeting_session():
    print(">>> DEBUG: run_greeting_session CALLED")
    name = get_nonempty_name()
    times = get_positive_number(f"How many times should {name} be greeted? ")

    greet(name, times)
    print()

    number = get_positive_number("Enter a number to generate its multiplication table: ")
    farewell_message = input("Enter a farewell message: ")

    table = save_table_to_file(name, times, number, farewell_message)
    print("Table saved to file.\n")

    for line in table:
        print(" ", line)
    print()

    custom_farewell(name, farewell_message)
    # NEW: increment session count
    session_number = increment_user_session(name)
    print(f"\nThis was session #{session_number} for {name}\n")


# --- Main Application Loop ---
def main():
    debug("entered main")

    sessions = []

    while True:
        show_menu()
        choice = input("Choose an option (A/B/C/D): ").strip().lower()

        if choice == "a":
             print(">>> DEBUG: run_greeting_session CALLED")
              
             name = get_nonempty_name()
             times = get_positive_number(f"How many times should {name} be greeted? ")

             greetings = greet(name, times)
             for line in greetings:
                print(line)

             number = get_positive_number("Enter a number to generate its multiplication table: ")
             farewell_message = input("Enter a farewell message: ")
             
             table = save_table_to_file(name, times, number, farewell_message)

             for line in table:
                 print(" ", line)

             
             farewell = custom_farewell(name, farewell_message)
             print(farewell)

        elif choice == "b":
             sessions = load_sessions()

             if not sessions:
              print("\nNo sessions saved yet.")
             else:
              print("\n--- Session Summary ---")
             for s in sessions:
              print(f"Name: {s['name']}")
              print(f"Greetings: {s['greetings']}")
              print(f"Table Number: {s['multiplication_number']}")
              print("-" * 20)

        elif choice == "c":
             sessions = load_sessions()
        elif choice == "d":
            print("\nAll sessions complete.")
            print("Thank you for using the Greeting App.")
            break
        if not sessions:
               print("\nNo sessions saved yet.")
        continue

    search_name = input("Enter name to search: ")

    matches = find_sessions_by_name(sessions, search_name)

    if not matches:
         print("\nNo sessions found for that user.")
    else:
        print("\n--- Matching Sessions ---")
        for s in matches:
            print(f"Name: {s['name']}")
            print(f"Greetings: {s['greetings']}")
            print(f"Table #: {s['multiplication_number']}")
            print("-" * 20)

    
    show_log = get_yes_no("Would you like to see the greetings log? (yes/no): ")
    if show_log == "yes":
        parsed_sessions = parse_greetings_log()

        if not parsed_sessions:
            print("\nNo sessions found in the greetings log.\n")
        else:
            print("\n--- All Sessions ---")
            display_parsed_sessions(parsed_sessions)

    search = get_yes_no("Would you like to search for sessions by user name? (yes/no): ")
    if search == "yes":
        search_name = get_nonempty_name()
        matched_sessions = find_sessions_by_name(parsed_sessions, search_name)

        if not matched_sessions:
            print(f"No sessions found for '{search_name}'.")
        else:
            print(f"\n--- Sessions for '{search_name}' ---")
            display_parsed_sessions(matched_sessions)

    print("\nThank you for using the Greeting App. Goodbye!")


# Program Entry Point
if __name__ == "__main__":
    main()