# main.py Notes:
# Main program logic
# Combines input, loops and functions

from functions import greet, farewell

name = input("Enter your name:")
times = int(input("How many greetings would you like?"))
                  
greet(name, times)
farewell(name)