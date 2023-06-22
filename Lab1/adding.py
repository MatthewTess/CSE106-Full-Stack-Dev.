def add_numbers():
    try:
        #Ask for a number to input
        user_input = input("Enter two or more numbers separated by spaces: ")
        numbers = user_input.split()
        if len(numbers) < 2:
            raise ValueError("You must enter two or more numbers") #Error if 2 or more numbers are not selected
        numbers = [float(num) for num in numbers]
        result = sum(numbers)
        print("The sum of the numbers: ", result) #Print sum
    except ValueError as ve:
        print(ve)

add_numbers()