import json


def writeToFile(dataDict, fileName):
    with open(fileName, 'w') as textFile:
        json.dump(dataDict, textFile)


if __name__ == '__main__':

    # Initial dictionary
    studentDataDict = dict()

    fileName = input("\nPlease enter the text file name: ")

    # Open the file
    try:

        with open(fileName) as f:
            studentDataDict = json.load(f)  # Loaded the dictionary data from text file
    except:

        print("\nCould not open text file " + fileName + ", please provide a correct file name.\n")
        exit()

    print("\nDictionary data got loaded from the file " + fileName + "\n")

    while True:

        print("\nMenu: \n\n1. Add a new Student \n2. Search for a student's grade \n3. Edit a grade \n4. Delete a grade")
        userChoice = input("\nEnter your choice: ")

        # Add a new student data to dictionary
        if userChoice == "1":

            studentName = input("\nEnter student name to add: ")

            # Check if the name already exists
            if studentName in studentDataDict:
                print("\nStudent name already exists, please enter a different name.\n")


            else:
                # Enter grade
                grade = float(input("\nEnter the student's grade: "))
                studentDataDict[studentName] = grade  # here we have added the new key to dictionary
                writeToFile(studentDataDict, fileName)
                print("\nNew Student added to data")


        elif userChoice == "2":

            studentName = input("\nEnter a student's name to find: ")

            if studentName not in studentDataDict:
                # Error if wrong name is provided
                print("\nNo student with this name found. Provide a valid student name\n")

            else:

                print(f"\nStudent Name: {studentName}\tGrade: {studentDataDict[studentName]}\n")


        elif userChoice == "3":

            studentName = input("\nEnter student name to update: ")

            if studentName not in studentDataDict:

                print("\nNo student with this name found. Provide a valid name\n")


            else:

                grade = float(input(f"\nEnter a new grade for {studentName}: "))
                studentDataDict[studentName] = grade  # updated the value for this key
                writeToFile(studentDataDict, fileName)
                print(f"\nGrade for student {studentName} has been updated")


        elif userChoice == "4":

            studentName = input("\nEnter a student name to delete: ")

            if studentName not in studentDataDict:

                print("\nNo student with this name in found. Provide a valid student name\n")


            else:

                # method remove this key from dictionary
                studentDataDict.pop(studentName)
                writeToFile(studentDataDict, fileName)
                print(f"\nGrade for student {studentName} is deleted.")


        elif userChoice == "5":

            writeToFile(studentDataDict, fileName)
            print("\nProgram closed.")

            break


        else:

            print("\nInvalid input. Try again.\n")
