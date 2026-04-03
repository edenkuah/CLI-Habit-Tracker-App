import datetime
from datetime import timedelta
import json

def load_habits():
    try:
        with open("habits.json", mode="r") as f:
            data = json.load(f)
            return data
        
    except FileNotFoundError:
        return []
    except Exception as e:
        return []

def save_data(habits):
    try:
        with open("habits.json", mode="w") as file:
            json.dump(habits, file)
    except FileNotFoundError:
        print("Error: File not found. Please Try Again.")
    except Exception as e:
        print(f"An error occured: {e}")

def add_habit():
    habits = load_habits()
    id = len(habits) + 1
    name = input("Input a habit: ")
    completed_dates = []

    new_habit = {
        "id": int(id),
        "name": name,
        "created_date": str(datetime.date.today()),
        "completed_dates": completed_dates
    }

    habits.append(new_habit)
    save_data(habits)
    print(f"\nSuccess! Added habit: {name} with ID: {id} \n")

def complete_habit_fetch():
    user_complete_id = input("Which habit have you completed today?(Input the ID) ")
    while True:
        if user_complete_id.strip() == "":
            print("--------------------------------------------\n"
            "Input cannot be empty. Please try again.")
            user_complete_id = input("Which habit have you completed today? ")
        elif user_complete_id.isalpha():
            print("--------------------------------------------\n"
            "Input must be a number(ID) . Please try again. \n"
            "--------------------------------------------")
            user_complete_id = input("Which habit have you completed today? ")
        else:
            return int(user_complete_id)

def complete_habit_print():
    all_habits = load_habits()
    for habit in all_habits:
        print("-------------------------------")
        print(f"{habit['id']}: ")
        print(f"Habit name: {habit['name']}")
         
def complete_habit(habit_id):
    found = False
    user_input = habit_id
    all_habits = load_habits()

    for habit in all_habits:
        if habit["id"] == user_input:
            print(f"Success! Changing completed status now. ID: {habit['id']} / Habit: {habit['name']}\n")
            if str(datetime.date.today()) not in habit["completed_dates"]:
                habit["completed_dates"].append(str(datetime.date.today()))
                found = True
            else:
                print("Already completed today")
                found = True

    save_data(all_habits)
    

    if not found:
        print("\n User ID input not found. \n")


def is_json_empty():
    try:
        data = load_habits()
        return not data
    except FileNotFoundError:
        return True
    except json.JSONDecodeError:
        return True
    
def view_all():
    if is_json_empty():
        print("No habits found. Please add a habit first.")
        return
    else:

        all_habits = load_habits()

        for habit in all_habits:
            # Streak calculation
            dates_list = sorted([datetime.date.fromisoformat(d) for d in habit["completed_dates"]])
            count = 0
            if dates_list:
                count = 1
                for i in range(len(dates_list) - 1):
                    if dates_list[i+1] - dates_list[i] == timedelta(days=1):
                        count += 1
                    else:
                        break

            # Completion rate
            created_date = datetime.date.fromisoformat(habit["created_date"])
            days_since_created = max((datetime.date.today() - created_date).days, 1)
            days_completed = len(habit["completed_dates"])
            completion_rate = (days_completed / days_since_created * 100)

            print(f"-------------------------------")
            print(f"Habit: {habit['name']} / ID: {habit['id']}")
            print(f"Streak: {count} days")
            print(f"Completion rate: {completion_rate:.0f}% ")
            print("-------------------------------")

def user_deletion_fetch():
    user_deletion_input = str(input("Enter the habit you would like to delete (Enter the ID): "))
    while True:
        if user_deletion_input.strip() == "":
            print("ID cannot be empty. Please try again.")
            user_deletion_input = str(input("Enter the habit you would like to delete (Enter the ID): "))
        elif user_deletion_input.isalpha():
            print("ID must be a number. Please try again.")
            user_deletion_input = str(input("Enter the habit you would like to delete (Enter the ID): "))
        else:
            return user_deletion_input
        
#Real function for deletion
def habit_deletion(habit_input):
    all_habits = load_habits()
    for habit in all_habits:
        if habit["id"] == int(habit_input):
            all_habits.remove(habit)
            save_data(all_habits)
            print("--------------------------------------------")
            print(f"\nSuccessful deletion of ID: {habit_input} habit: {habit['name']} \n")
            print("--------------------------------------------")



while True:
    print("1. Add a habit")
    print("2: Mark a habit as completed")
    print("3: View all habits and stats")
    print("4: Delete a habit")
    print("5: Exit")
    option = str(input("Select an option (1 To 5): "))
    if option == "1" or option.lower() == "add" or option.lower() == "add habit":
        add_habit()
    elif option == "2" or option.lower() == "complete" or option.lower() == "complete habit":
        print("Here are all your habits: ")
        view_all()
        complete_habit_print()
        completed_habit = complete_habit_fetch()
        complete_habit(completed_habit)
    elif option == "3" or option.lower() == "view" or option.lower() == "view all":
        view_all()
    elif option == "4" or option.lower() == "delete" or option.lower() == "delete habit":
        print("Here are all your habits: ")
        view_all()
        user_habit_input = user_deletion_fetch()
        habit_deletion(user_habit_input)
    elif option == "5" or option.lower() == "exit":
        print("--------------------------------------------")
        print("          Exiting the app. Goodbye!")
        print("--------------------------------------------")
        break
    else:
        error_msg1 = (f"Invalid Input! Please try again!")
        print("-" * (len(error_msg1) + 10))
        print((" " * 5) + error_msg1)
        print("-" * (len(error_msg1) + 10))
        