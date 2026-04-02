import datetime
from datetime import timedelta
import json

todays_date = str(datetime.date.today())
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
        "created_date": todays_date,
        "completed_dates": completed_dates
    }

    habits.append(new_habit)
    save_data(habits)

def complete_habit_fetch():
    user_complete_id = input("Which habit have you completed today?(Input the ID) ")
    while True:
        if user_complete_id.strip() == "":
            print("--------------------------------------------\n"
            "Input cannot be empty. Please try again.")
            user_complete_id = input("Which habit have you completed today? ")
        elif not user_complete_id.isdigit():
            print("--------------------------------------------\n"
            "Input must be a number(ID) . Please try again.")
            user_complete_id = input("Which habit have you completed today? ")
        else:
            return int(user_complete_id)

def complete_habit(id):
    found = False
    user_input = id
    all_habits = load_habits()
    for habit in all_habits:
        print("-------------------------------")
        print(f"{habit['id']}: ")
        print(f"Habit name: {habit['name']}")

    for habit in all_habits:
        if habit["id"] == user_input:
            print(f"Success! Changing completed status now. ID: {habit['id']}")
            if todays_date not in habit["completed_dates"]:
                habit["completed_dates"].append(todays_date)
                found = True

    save_data(all_habits)
            
    if not found:
        print("User ID input not found.")

def view_all():
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
                    count = 0

        # Completion rate
        created_date = datetime.date.fromisoformat(habit["created_date"])
        days_since_created = (datetime.date.today() - created_date).days
        days_completed = len(habit["completed_dates"])
        completion_rate = (days_completed / days_since_created * 100) if days_since_created > 0 else 0

        print(f"-------------------------------")
        print(f"Habit: {habit['name']}")
        print(f"Streak: {count} days")
        print(f"Completion rate: {round(completion_rate)}%")
        print("-------------------------------")

def delete_habit():
    print("-" * 70 + "\n"
        "Delete habit function is currently unavailable. Please stay tuned for updates."
        "\n" + "-" * 70)


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
        completed_habit = complete_habit_fetch()
        complete_habit(completed_habit)
    elif option == "3" or option.lower() == "view" or option.lower() == "view all":
        view_all()
    elif option == "4" or option.lower() == "delete" or option.lower() == "delete contact":
        delete_habit()
    elif option == "5" or option.lower() == "exit":
        break
    else:
        print(f"Invalid Input! Please try again!")