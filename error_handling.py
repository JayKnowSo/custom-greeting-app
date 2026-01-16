# Error handling basics

try:
    number = int(input("Enter a number: "))
    print(f"You entered: {number}")
except:
    print("That's not a valid number!")