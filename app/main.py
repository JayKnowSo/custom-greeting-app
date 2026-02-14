"""Main runner for the Custom Greeting App.

This module coordinates user interaction and uses helper functions
from the project to generate greetings and multiplication tables.
"""
# Greeting App main.py - Controls flow and menus, calls functions from functions.py

from app.infrastructure.functions import (
    greet,
    custom_farewell,
    load_sessions,
    save_sessions,
    save_table_to_file,
    find_sessions_by_name,
    compute_session_stats,

    
)
from helpers import get_nonempty_name, get_positive_number, get_yes_no

# --- Debug Helper ---
DEBUG = False  # Set True to see debug messages

def debug(msg):
    """Print debug messages only if DEBUG is True."""
    if DEBUG:
        print(f"[DEBUG] {msg}")

def show_menu():
    print("\n=== Greeting App Menu ===")
    print("A) Start a greeting session")
    print("B) View session count per user")
    print("C) Search sessions by name")
    print("D) Exit")
    print("E) Show session statistics")

# --- Main Application Loop ---
def main():
    debug("entered main")

    sessions = []

    while True:
        show_menu()
        choice = input("Choose an option (A/B/C/D/E): ").strip().lower()

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

        elif choice == "d":
          print("\nAll sessions complete.")
          print("Thank you for using the Greeting App.")
          break

        elif choice == "e":
            sessions = load_sessions()

            if not sessions:
                print("\nNo sessions saved yet.")
                continue

            stats = compute_session_stats(sessions)

            print("\n--- Session Statistics ---")
            print(f"Total sessions: {stats['total_sessions']}")
            print(f"Total greetings: {stats['total_greetings']}")
            print(f"Unique users: {stats['unique_users']}")
            print(f"Most used multiplication number: {stats['most_used_number']}")
            print("-" * 30)

# Program Entry Point
if __name__ == "__main__":
    main()