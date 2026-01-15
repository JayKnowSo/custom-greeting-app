# main.py Notes:
from functions import greet, custom_farewell

while True: # Loop for multiple sessions
    name = input("Enter your name:")
    times = int(input("How many times would you like to be greeted?"))

    greet(name, times)

    farewell_message = input("Enter a farewell message:")
    custom_farewell(name, farewell_message)

    repeat = input("Do you want to run another session? (yes/no):").lower()
    if repeat != "yes":
     print("Exiting the program. Goodbye!")
     break 