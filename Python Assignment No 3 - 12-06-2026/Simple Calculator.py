def addition (num1,num2):
    return num1+num2

def subtraction (num1,num2):
    return num1-num2

def multiplication (num1,num2):
    return num1*num2

def division (num1,num2):
    if num2 == 0:
        return "Error: Cannot divde by zero"
    return num1/num2

while True:
        print("\nSimple Calculator")
        print("1: Addition")
        print("2: Subtraction")
        print("3: Multiplication")
        print("4: Division")
        print("5: Exit")

        choice = input("Enter your choice 1-5: ")

        if choice in ["1","2","3","4"]:
            try:
                 num1 = float(input("Enter the first number: "))
                 num2 = float(input("Enter the second number: "))
            except ValueError:
                 print("Error: Please enter a valid number")
                 continue
        
        if choice == "1":
             result = addition (num1,num2)
             print(f"Result: {result}")
        elif choice == "2":
             result = subtraction(num1,num2)
             print(f"Result: {result}")
        elif choice == "3":
             result = multiplication(num1,num2)
             print(f"Result: {result}")
        elif choice == "4":
             result = division(num1,num2)
             print(f"Result: {result}")
        
        elif choice == "5":
             break
        else:
             print("Invalid choice: Please choose between 1-5")
