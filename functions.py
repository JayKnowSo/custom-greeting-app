# functions.py
# Notes: All reusable code lives here
# Functions return values or print messages

def greet(name, times):
    for i in range(times):
            print(f"Hello {name}! (greeting {i+1})")
        
def farewell(name):       
        print(f"Goodbye {name}! See you next time, see ya!")