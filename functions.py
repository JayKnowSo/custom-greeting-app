# functions.py
# Notes: All reusable code lives here
# Functions return values or print messages

def greet(name, times):
    for i in range(times):
       print(f"Hello {name}! (greeting {i+1})")

def farewell(name):
       print(f"Goodbye {name}! See you next time!")
        
def custom_farewell(name, farewell_message):       
       print(f"{farewell_message}, {name}!")

def save_table_to_file(name, number, table):
    """Saves the multiplication table to a log file."""
    filename = f"{name}_multiplication_table.txt"
    with open("greetings_log.txt", "a") as file:
        file.write(f"{name}'s multiplication table for {number}:\n")
        for line in table:
            file.write(line + "\n")
        file.write("-" * 30 + "\n")  # Add a newline for separation

def read_greetings_log():
             """Reads and prints the contents of greetings_log.txt"""
             try:
                 with open("greetings_log.txt", "r") as file:
                     return file.read()
             except FileNotFoundError:
                 return "The greetings log file does not exist yet."
             
def parse_greetings_log():
    """parse greetings_log.txt into structured data."""
    sessions = []
    current_session = None
    
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
                elif " x " in line and current_session:
                        current_session["table"].append(line)
                else:
                    current_session = {
                        "name": line,
                        "table": []
                   }
                
        if current_session:
             sessions.append(current_session)
    except FileNotFoundError:
         pass
    return sessions