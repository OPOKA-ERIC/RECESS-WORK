# Functions

def add(num1, num2):
    return num1 + num2


def subtract(num1, num2):
    return num1 - num2


def multiply(num1, num2):
    return num1 * num2


def divide(num1, num2):

    if num2 == 0:
        return "Division by zero is not allowed."

    return num1 / num2


# Main program
while True:

    print("\n===== CALCULATOR MENU =====")
    print("1. Addition")
    print("2. Subtraction")
    print("3. Multiplication")
    print("4. Division")
    print("5. Exit")

    choice = input("Enter your choice: ")

    if choice == "5":
        print("Thank you for using the calculator.")
        break

    if choice == "1" or choice == "2" or choice == "3" or choice == "4":

        num1 = float(input("Enter first number: "))
        num2 = float(input("Enter second number: "))

        if choice == "1":
            answer = add(num1, num2)
            print(f"Answer = {answer}")

        elif choice == "2":
            answer = subtract(num1, num2)
            print(f"Answer = {answer}")

        elif choice == "3":
            answer = multiply(num1, num2)
            print(f"Answer = {answer}")

        elif choice == "4":
            answer = divide(num1, num2)
            print(f"Answer = {answer}")

    else:
        print("Invalid choice.")