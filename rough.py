print("Daily Habit Tracker by Parth")
name= input("please enter your name:")

import json
import os
from datetime import datetime
1
DATA_FILE = 'habits.json'
DATE_FORMAT = '%Y-%m-%d'


def load_habits():
    """Loads habit data from the JSON file. Creates an empty file if it doesn't exist."""
    if not os.path.exists(DATA_FILE):
        print(f"[{DATA_FILE}] not found. Starting with a new habit list.")
        return {}
    
    try:
        with open(DATA_FILE, 'r') as f:
  
            data = json.load(f)
        
            return data if isinstance(data, dict) else {}
    except json.JSONDecodeError:
        print(f"Error reading [{DATA_FILE}]. File might be corrupted. Starting new data.")
        return {}
    except Exception as e:
        print(f"An unexpected error occurred while loading data: {e}")
        return {}

def save_habits(habits):
    """Saves the current habit data to the JSON file."""
    try:
        with open(DATA_FILE, 'w') as f:
            json.dump(habits, f, indent=4)
        print("Data saved successfully.")
    except Exception as e:
        print(f"Error saving data: {e}")

def add_habit(habits):
    """Allows the user to add a new habit."""
    name = input("Enter the name of the new habit: ").strip()
    
    if not name:
        print("Habit name cannot be empty.")
        return

    habit_key = name.lower().replace(' ', '_')
    
    if habit_key in habits:
        print(f"Habit '{name}' already exists!")
        return

    habits[habit_key] = {
        'name': name,
        'created_at': datetime.now().strftime(DATE_FORMAT),
        'log': []
    }
    print(f"Habit '{name}' added successfully!")

def log_completion(habits):
    """Allows the user to log a completion for an existing habit."""
    if not habits:
        print("No habits added yet. Please add a habit first (Option 1).")
        return

    print("\n--- Available Habits ---")
    keys = list(habits.keys())
    for i, key in enumerate(keys):
        print(f"  {i+1}. {habits[key]['name']}")
    
    choice = input("Enter the number of the habit you completed today: ").strip()
    
    try:
        index = int(choice) - 1
        if 0 <= index < len(keys):
            habit_key = keys[index]
            
            today_date = datetime.now().strftime(DATE_FORMAT)
            habit_data = habits[habit_key]
            
            if today_date in habit_data['log']:
                print(f"You already logged '{habit_data['name']}' completion today ({today_date}).")
            else:
                habit_data['log'].append(today_date)
                print(f"Successfully logged completion for '{habit_data['name']}' on {today_date}.")
        else:
            print("Invalid number entered.")
    except ValueError:
        print("Invalid input. Please enter a number.")


def view_status(habits):
    """Displays the status of all habits, including the log count and last completed date."""
    if not habits:
        print("No habits to display. Please add a habit first.")
        return

    print("\n==================================")
    print("      HABIT TRACKER STATUS")
    print("==================================")
    
    for habit_key, data in habits.items():
        name = data['name']
        log_count = len(data['log'])
        
        last_log = "Never"
        if log_count > 0:
           
            last_log = sorted(data['log'])[-1]

        print(f"\nHabit: {name}")
        print(f"  - Total Completions: {log_count}")
        print(f"  - Last Completed: {last_log}")
        
    print("\n==================================")

def main():
    """Main function to run the Habit Tracker application."""
    habits = load_habits()
    
    while True:
        print("\n=== Simple Habit Tracker ===")
        print("1. Add New Habit")
        print("2. Log Habit Completion (Today)")
        print("3. View All Habit Status")
        print("4. Save & Exit")
        
        choice = input("Enter your choice (1-4): ").strip()
        
        if choice == '1':
            add_habit(habits)
        elif choice == '2':
            log_completion(habits)
        elif choice == '3':
            view_status(habits)
        elif choice == '4':
            save_habits(habits)
            print("Thank you for using the tracker. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 4.")

if __name__ == "__main__":
    main()