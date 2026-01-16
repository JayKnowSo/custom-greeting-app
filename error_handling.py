# Error handling basics
# Error part 2: try/ except/ else/ finally demonstration

try:
    number = int(input("Enter a number: "))
except ValueError:
    print("Please enter a valid number!.")
else:
    print(f"You entered the number: {number}, which is valid!")
finally:
    print("This always runs, regardless of errors.")