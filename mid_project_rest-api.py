import requests

SERVER_PORT = 5000
SERVER_URL = "http://52.55.144.116:" + str(SERVER_PORT)
STUDENTS_API = "students"

def getStudentsFullUrl():
    return SERVER_URL + "/" + STUDENTS_API

def displayMenu():
    print("\n--- Main Menu ---")
    print(" 1. Get student list ")
    print(" 2. Get a specific student information ")
    print(" 3. Save a new student ")
    print(" 4. Change student name ")
    print(" 5. Change student age ")
    print(" 6. Delete student ")
    print(" 7. Exit system") 
     
def handleChoice(choice):
    if choice == '1':
       return getStudentList()
    elif choice == '2':
        getSpecificStudent()
    elif choice == '3':
        SaveNewName()
    elif choice == '4':
        ChangeName()
    elif choice == '5':
        ChangeAge()
    elif choice == '6':
        deleteStudent()
    elif choice == '7':
        exitSystem()
        if exitSystem(): 
            return -2
    else:
        print("Option " + choice + " does not exist. Please try again.")
    return -1



def main():
    while True:
        displayMenu()
        choice = input("Please enter your choice: ")
        print()
        handlechoice_result = handleChoice(choice)
        if handlechoice_result == -2:
            return
        input("Press enter to continue ")
        print()


# פונקציה להדפסת פרטי סטודנט
def printStudentInfo(student):
    print()
    print("--- Student Information ---")
    print("---------------------------")
    print("id: " + str(student['id']))
    print("name: " + student['name'])
    print("age: " + str(student['age']))
    print("---------------------------")
    print()


 # בקשה כללית להדפסת סטודנטים - GET
def getStudentList(): # Option 1
    response = requests.get(getStudentsFullUrl())
    if response.status_code == 200:
        students = response.json()["students"]
        print("--- Student Information ---")
        print("---------------------------")
        for student in students:
            print("id: " + str(student['id']))
            print("name: " + student['name'])
            print("age: " + str(student['age']))
            print("---------------------------")
            print()
    else:
        print("Error: Could not fetch students")
      

 # בקשה להדפסת סטודנט ספציפי - GET
def getSpecificStudent():  # Option 2
    specific_id = input("Enter the student ID: ")
    if not specific_id.isdigit():
        print("The " + specific_id + " is not a number, please Try again ")
        return -1
    specific_id = int(specific_id)
    response = requests.get(getStudentsFullUrl())
    if response.status_code == 200:
        students = response.json()["students"]
        for student in students:
            if student['id'] == specific_id:  # אם ה-ID של הסטודנט תואם לזה שהמשתמש הזין
                printStudentInfo(student)
                return  # יוצאים מהלולאה אחרי שמצאנו את הסטודנט
        print("Student with ID " + str(specific_id) + " not found.")
 

 # הוספת שם חדש - POST 
def SaveNewName():    # Option 3
    name = input("Enter the full student name: ")
    age = input("Enter the student age: ")
    if not age.isdigit():
        print("The age must be a number. Please try again.")
        return -1
        # יצירת דיקט של הנתונים כדי לשלוח ל-API
    data = {"name": name, "age": int(age)}
    response = requests.post(getStudentsFullUrl(), json=data)
    if response.status_code == 201:
        print("student Created successfuly" )
        student = response.json()
        printStudentInfo(student)
    else:
        # במקרה של שגיאה
        print("Error: Creation Failed")


 # שינוי שם סטודנט - PUT
def ChangeName():  # Option 4
    id = input("Enter the student ID: ")
    url = getStudentsFullUrl() + "/" + str(id)
    response = requests.get(url)
    if response.status_code != 200: 
        print("Student with ID " + str(id) + " not found.")
        return
    new_name = input("Enter the new student name: ")
    student = response.json()
    data = {"name": new_name, "age": student['age']}
    response = requests.put(url, json=data)
    if response.status_code == 200:
        print("Student name updated successfully")
    else:
        print("Error: Update Failed")


 # שינוי גיל סטודנט - PUT
def ChangeAge():   # Option 5
    id = input("Enter the student ID: ")
    url = getStudentsFullUrl() + "/" + str(id)
    response = requests.get(url)
    if response.status_code != 200:
        print("Student with ID " + str(id) + " not found.")
        return
    new_age = input("Enter the new student age: ")
    if  new_age.isdigit():
        age = int(new_age)  # המרת הגיל למספר
    else:
        print("Please enter a valid number for age.")
        return   
    response = requests.get(url)
    if response.status_code == 200:
        student = response.json()
        name = student['name']
        data = {"name": name, "age": age}
        response = requests.put(url, json=data)
        if response.status_code == 200:
            student = response.json()
            printStudentInfo(student)
        else:
            print("Error: Update Failed")


 # בקשת DELETE
def deleteStudent():  # Option 6
    id = input("Enter the student ID: ")
    url = getStudentsFullUrl() + "/" + str(id)
    response = requests.get(url)  # קודם נוודא שהסטודנט קיים
    if response.status_code != 200:  # אם הסטודנט לא נמצא
        print("Student with ID " + str(id) + " not found.")
        return
    response = requests.delete(url)
    if response.status_code == 200:
        print("Delete successful")
    else: 
        print("Error: Delete failed")



# יציאה מהמערכת
def exitSystem(): # Option 7
    while True: 
        user_input = input("Are you sure you want to exit? y/n: ")
        if user_input == "y":
            print("Ok, goodbye")
            return True 
        elif user_input == "n":
            return False
        else:
            print("Invalid input, please enter 'y' or 'n'.")


main()

