from class_person import Person
from class_employee import Employee
from class_student import Student
from class_menuItems import MenuItems
import pandas as pd
import os
# print(os.getcwd)
import utils


def displayMenu():
    for item in MenuItems:
        print(str(item.value) + ". " + item.name)  # Printing each menu item


def handleChoice(selected_choice, people_dict, total_age):
    if selected_choice == MenuItems.SAVE_A_NEW_ENTRY:
        return saveNewEntry(people_dict)
    elif selected_choice == MenuItems.SEARCH_BY_ID:
        searchById(people_dict)
    elif selected_choice == MenuItems.PRINT_ALL_NAME:
        printAllName(people_dict)
    elif selected_choice == MenuItems.PRINT_AGES_AVERAGE:
        printAverageAge(people_dict, total_age)
    elif selected_choice == MenuItems.PRINT_ALL_IDS:
        printAllId(people_dict)
    elif selected_choice == MenuItems.PRINT_ALL_ACCOUNTS:
        printAllAccounts(people_dict)
    elif selected_choice == MenuItems.PRINT_ENTRY_BY_INDEX:
        printItemByIndex(people_dict)
    elif selected_choice == MenuItems.SAVE_ALL_DATA:
        saveAllData(people_dict)
    elif selected_choice ==MenuItems.EXIT: 
        if exitSystem(): 
            return -2
    else:
        print("Option " + str([selected_choice]) + " does not exist. please try again")
    return -1
    

def main():
    people_dict = {}
    total_age = 0
    while True:
        displayMenu()
        try:
            selected_choice = MenuItems(int(input("Please enter your choice: ")))   
            handlechoice_result = handleChoice(selected_choice, people_dict, total_age)
            if handlechoice_result == -2:
                return
            else:
                if handlechoice_result > 0:
                    total_age += handlechoice_result
        except ValueError:
            print("Error: Error: Invalid number or character entered. Please try again.") 
        input("Press enter to continue ")
        


def saveNewEntry(people_dict):  # Option 1
    while True:
        human_personality = input("Please write what are you Employee(press 1) or Student(press 2)? : ") 
        if human_personality == "1":
            person_info = Employee()
            break
        elif human_personality == "2":
            person_info = Student()
            break
        else:
            print("Invalid choice, please try again.")
    if not person_info.userSurvey():
        return -1
    if not utils.isDigit:
        return -1
    if person_info.getId() in people_dict:
        print("The " + str([person_info.getId()]) + " exists in the system, please try again ")
        return -1            
    people_dict[person_info.getId()] = person_info
    print("ID " + str([person_info.getId()]) + " seved successfully")
    return person_info.getAge() # Returns age, for calculating average ages on Option 3           
    

def searchById(data_dict): # option 2
    entry_id = input("please enter the ID you are looking for: ")
    try:
        entry_id = int(entry_id)  
    except ValueError:
        print("The ID " + str([entry_id])  + " is not a number please try again")
        return
    if entry_id in data_dict:
      person_info = data_dict[entry_id]
      person_info.printPersons()
    else: 
        print("Error: ID " + str([entry_id])+ " Does not exist please try again ") 
        
    
def printAverageAge(persons_info, total_age):  # Option 3
    if not persons_info:
        print("No entries found please try again")
        return
    average_age = total_age / len(persons_info)
    print("The average age is " + str(average_age) + " years.")
   

def printAllName(data_dict):  # option 4
    for index, person_id in enumerate(data_dict):
        persons_info = data_dict[person_id]
        name = persons_info.getName()
        print(str(index) +". "+ name)


def printAllId(data_dict):  # option 5
    for index, person_id in enumerate(data_dict):
        print(str(index) +". " + str(person_id))


def printAllAccounts(data_dict):  # option 6
    for index, person_id in enumerate(data_dict): 
        print(str(index) + ". " + str(person_id))   
        persons_info = data_dict[person_id]
        persons_info.printPersons()    


def printItemByIndex(data_dict): # option 7
    index_from_user = input("please enter the index of the entry you want to print: ")
    last_index = len(data_dict) - 1
    if not index_from_user.isdigit():
       print("The index " + str([index_from_user]) + " is not a number please try again")
       return
    index_from_user_int = int(index_from_user)
    if index_from_user_int > last_index:
        print("The index " + str([index_from_user]) + " out of range, max index it " + str([last_index]) + " please try again")
        return
    for index, person_id in enumerate(data_dict):
        if index == index_from_user_int:
            print(str(index) + ". ")    
            person_info = data_dict[person_id]
            person_info.printPersons() 


def saveAllData(people_dict): # Option 8
    file_name_output = input("What is your output file name? ")
    try:
        if file_name_output == "":
           raise ValueError       
        if file_name_output[-4:] != ".csv":
           file_name_output += ".csv"
        data_list = []
        for person_id, details in people_dict.items():
           data_list.append(details.getPersonDict())
        df = pd.DataFrame(data_list)
        df.to_csv(file_name_output, index=False)
        print("Data saved to " + file_name_output)
    except ValueError:  
        print("Error: You did not write a file name.")


def exitSystem(): # Option 9
    while True: 
        user_input = input("Are you sure you want to exit? y/n: ")
        if user_input == "y":
            print("Ok, goodbye")
            return True 
        elif user_input == "n":
            return False
    
        

main()





