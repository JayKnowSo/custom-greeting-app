# Notes: Refactored Greeting App with Input Validation, Else/Finally and Helpers

# Import project functions and helpers
from functions import greet, custom_farewell, save_table_to_file, read_greetings_log, parse_greetings_log
from helpers import get_nonempty_name, get_positive_number, get_yes_no
from math_tables import get_multiplication_table

# Multi-session tracking
all_sessions = [] # List  will store dictionaries of each user session's data

while True:
    name = get_nonempty_name()  # Get a valid name from user
    times = get_positive_number("How many times would you like to be greeted? ")

    greet(name, times)  # Greet the user specified number of times
    print() # Spacing

    number = get_positive_number("Enter a number to generate its multiplication table: ")
    table = get_multiplication_table(number)
    for line in table:
        print(line)
        
    save_table_to_file(name, number, table)  # Save multiplication table to file
    print("Table saved to file.\n")

    session = {
        "name": name,
        "greetings": times,
        "multiplication_number": number,
        "multiplication_table": table
    }
    all_sessions.append(session)  # Store session data

    farewell_message = input("Enter a farewell message: ")
    custom_farewell(name, farewell_message)
    print()  # Spacing

    repeat = get_yes_no("Would you like to run the session again? (yes/no): ")
    
    if repeat == "no":
        print("Thank you for using the Greeting App. Goodbye!")

        show_log = get_yes_no("would you like to see the greetings log? (yes/no):")
        if show_log == "yes":
            log_contents = read_greetings_log()
            print("\n--- Greetings Log ---")
            print(log_contents)

            parsed_sessions = parse_greetings_log()
            print("\n---parases sessions ---")
            for session in parsed_sessions:
                print(f"name: {session['name']}")
                for line in session["table"]:
                    print("", line)
        break  # Exit the loop and end the program