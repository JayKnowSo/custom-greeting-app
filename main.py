# Notes: Refactored Greeting App with Input Validation, Else/Finally and Helpers

# Import project functions and helpers
from functions import greet, custom_farewell
from helpers import get_nonempty_name, get_positive_number, get_yes_no
from file_utils import save_greetings
from math_tables import get_multiplication_table

while True:
    name = get_nonempty_name()  # Get a valid name from user
    times = get_positive_number("How many times would you like to be greeted? ")

    greet(name, times)  # Greet the user specified number of times
    save_greetings(name, times)  # log the session

    farewell_message = input("Enter a farewell message: ")
    custom_farewell(name, farewell_message)

    print()  # Spacing

    repeat = get_yes_no("Would you like to run the session again? (yes/no): ")
    if repeat == "no":
        print("Thank you for using the Greeting App. Goodbye!")
        break