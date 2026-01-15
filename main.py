# main.py Notes:
# Main program logic
# Combines input, loops and functions

from functions import greet, farewell, custom_farewell

name = input("Enter your name:")
times = int(input("How many greetings would you like?"))
                  
greet(name, times)

# Ask user for a custom farewell
farewell_message = input ("Enter a farewell message:") 
custom_farewell(name, farewell_message)