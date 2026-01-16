# Notes: Responsible for saving greeting logs to a file

def save_greetings(name, times):
    with open("greeting_log.txt", "a") as file:
        file.write(f"User: {name}\n")
        file.write(f"Greetings count: {times}\n")
        file.write("-" * 25 + "\n")