from functions import greet, custom_farewell

while True:  # Loop for multiple sessions
    name = input("Enter your name:")
    try:
        times = int(input("How many times would you like to be greeted?"))
        if times <= 0:
            print("Please enter a number greater than 0.")
            continue
    except ValueError:
        print("Invalid input. Please enter a valid number.")
        continue

    greet(name, times)

    farewell_message = input("Enter a farewell message:")
    custom_farewell(name, farewell_message)

    repeat = input("Do you want to run another session? (yes/no):").lower()
    if repeat != "yes":
        print("Exiting the program. Goodbye!")
        break