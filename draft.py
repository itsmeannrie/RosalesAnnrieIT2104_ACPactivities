import datetime
import json
from collections import defaultdict
from enum import Enum

# Store all expenses in a list
expenses = []
user_info = {
    "name": "",
    "savings_account": 0.0,
    "monthly_budgets": {}
}

class Category(Enum):
    FOOD = "Food"
    TRANSPORT = "Transport"
    ENTERTAINMENT = "Entertainment"
    UTILITIES = "Utilities"
    OTHER = "Other"

# Utility Functions
def get_valid_amount(prompt):
    """Prompt user for a numeric input and validate."""
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Invalid input. Please enter a numeric value.")

def get_date_input():
    """Prompt user for a valid date input in MM-DD-YYYY format."""
    while True:
        date_str = input("Enter date (MM-DD-YYYY): ")
        try:
            return datetime.datetime.strptime(date_str, "%m-%d-%Y").date()
        except ValueError:
            print("Invalid date format. Please enter in MM-DD-YYYY format.")

def select_category():
    """Prompt user to select a category from predefined options."""
    print("\nCategories:")
    for idx, category in enumerate(Category, start=1):
        print(f"{idx}. {category.value}")
    while True:
        choice = input("Choose a category number: ")
        if choice.isdigit() and 1 <= int(choice) <= len(Category):
            return list(Category)[int(choice) - 1].value
        print("Invalid choice. Please select a valid category number.")

# Expense Management Functions
def load_expenses():
    """Load expenses and user info from a JSON file."""
    global expenses, user_info
    try:
        with open("expenses.json", "r") as file:
            data = json.load(file)
            expenses = data.get("expenses", [])
            
            # Convert the string keys back to (year, month) tuple
            user_info.update(data.get("user_info", {}))
            if "monthly_budgets" in user_info:
                user_info["monthly_budgets"] = {
                    tuple(map(int, key.split('-'))): value
                    for key, value in user_info["monthly_budgets"].items()
                }
            print("\n------Expenses and budget loaded successfully. ------")
    except FileNotFoundError:
        print("\n------No saved data found. Starting fresh. ------")
    except json.JSONDecodeError:
        print("\n------Data corrupted. Starting fresh. ------")

def save_expenses():
    """Save expenses and user info to a JSON file."""
    try:
        # Convert the (year, month) tuple keys back to string for JSON serialization
        user_info["monthly_budgets"] = {
            f"{year}-{month:02d}": budget
            for (year, month), budget in user_info["monthly_budgets"].items()
        }
        
        with open("expenses.json", "w") as file:
            json.dump({"expenses": expenses, "user_info": user_info}, file)
            print("----- Data saved successfully. -----")
    except IOError as e:
        print(f"An error occurred while saving data: {e}")
    finally:
        # Restore monthly_budgets format for further use
        user_info["monthly_budgets"] = {
            (int(year_month.split("-")[0]), int(year_month.split("-")[1])): budget
            for year_month, budget in user_info["monthly_budgets"].items()
        }

def set_user_budget():
    """Prompt user to set a monthly budget."""
    year = datetime.datetime.now().year
    month = datetime.datetime.now().month
    monthly_budget = get_valid_amount(f"Enter your budget for {datetime.datetime(year, month, 1).strftime('%B %Y')}: ")
    user_info["monthly_budgets"][(year, month)] = monthly_budget
    print(f"Budget for {datetime.datetime(year, month, 1).strftime('%B %Y')} set to: ₱{monthly_budget:.2f}")
    save_expenses()

def modify_monthly_budget():
    """Allow the user to modify the budget for a specific month."""
    print("\nModify Monthly Budget:")
    try:
        year_input = input("Enter the year (e.g., 2024): ")
        if not year_input.isdigit():
            print("Invalid year. Please enter a valid 4-digit number (e.g., 2024).")
            return
        year = int(year_input)
        
        month_input = input("Enter the month number (1-12): ")
        if not month_input.isdigit():
            print("Invalid month. Please enter a number between 1 and 12.")
            return
        month = int(month_input)
        
        if not (1 <= month <= 12):
            print("Invalid month. Please enter a number between 1 and 12.")
            return
        
        monthly_budget = get_valid_amount(f"Enter the new budget for {datetime.datetime(year, month, 1).strftime('%B %Y')}: ")
        user_info["monthly_budgets"][(year, month)] = monthly_budget
        print(f"Budget for {datetime.datetime(year, month, 1).strftime('%B %Y')} updated to: ₱{monthly_budget:.2f}")
        save_expenses()
    except ValueError:
        print("Invalid input. Please enter valid numeric values for year and month.")

def reset_data():
    """Reset all expenses and user information."""
    global expenses, user_info
    expenses.clear()  
    user_info = {  
        "name": "",
        "savings_account": 0.0,
        "monthly_budgets": {}
    }
    save_expenses()
    print("All data has been reset.")
    print("Please set a new budget before proceeding.")
    set_user_budget()

def add_expense():
    """Prompt user to add a new expense with validation and budget check."""
    if not user_info["monthly_budgets"]:
        print("No budget set for the current month. Please set a budget first.")
        set_user_budget()
    
    print("\n--- Adding a New Expense ---")
    category = select_category()
    description = input("\nEnter expense description: ")
    amount = get_valid_amount("Enter expense amount: ")
    date = get_date_input()

    expense = {
        "description": description,
        "amount": amount,
        "date": date.strftime("%m-%d-%Y"),
        "category": category
    }
    expenses.append(expense)
    save_expenses()

    print("\nNew Expense Added:")
    print(f"  Description: {description}")
    print(f"  Amount: ₱{amount:.2f}")
    print(f"  Date: {date.strftime('%m-%d-%Y')}")
    print(f"  Category: {category}")

def view_expenses():
    """Display all expenses."""
    if not expenses:
        print("No expenses found.")
        return
    
    print("\n------ List of Expenses: ------")
    for idx, expense in enumerate(expenses, start=1):
        print(f"{idx}. {expense['description']} - ₱{expense['amount']} on {expense['date']} [{expense['category']}]")

def delete_expense():
    """Prompt user to delete an expense by its index."""
    if not expenses:
        print("No expenses to delete.")
        return

    try:
        index = int(input("\nEnter the number of the expense to delete: ")) - 1
        if 0 <= index < len(expenses):
            deleted = expenses.pop(index)
            print(f"Deleted expense: {deleted['description']} - ₱{deleted['amount']} on {deleted['date']} [{deleted['category']}]")
            save_expenses()
        else:
            print("Invalid number. Please try again.")
    except ValueError:
        print("Please enter a valid number.")

def generate_report():
    """Generate a report of monthly expenses with budget warnings."""
    if not expenses:
        print("No expenses found. Please add some expenses to generate a report.")
        return

    print("\nExpense Report by Month and Year")
    monthly_expenses = defaultdict(lambda: defaultdict(float))
    for expense in expenses:
        date = datetime.datetime.strptime(expense["date"], "%m-%d-%Y")
        year_month = (date.year, date.month)
        category = expense["category"]
        monthly_expenses[year_month][category] += expense["amount"]

    for (year, month), categories in sorted(monthly_expenses.items()):
        month_name = datetime.datetime(year, month, 1).strftime('%B %Y')
        print(f"\n--- Report for {month_name} ---")
        monthly_total = sum(categories.values())
        for category, total in categories.items():
            print(f"  {category}: ₱{total:.2f}")
        print(f"  Total for {month_name}: ₱{monthly_total:.2f}")
        
        budget = user_info["monthly_budgets"].get((year, month), 0)
        remaining_budget = budget - monthly_total
        print(f"  Budget for {month_name}: ₱{budget:.2f}")
        print(f"  Remaining budget for {month_name}: ₱{remaining_budget:.2f}")
        
        if remaining_budget < 0:
            print(f"  Warning: Over budget by ₱{-remaining_budget:.2f}!")

def display_menu():
    """Display the main menu and return the user's choice."""
    print("\nXPENSE TRACKER MENU")
    print("1. Modify Monthly Budget")
    print("2. Add Expense")
    print("3. View List of Expenses")
    print("4. Delete Expense")
    print("5. Generate Monthly Report")
    print("6. Reset Data")
    print("7. Exit")
    return input("Choose an option: ")

# Main Program 
def main():
    print("╔" + "═" * 30 + "╗")
    print("║{:^30}║".format("Welcome to Xpense Tracker"))
    print("╚" + "═" * 30 + "╝")
    user_info["name"] = input("\nPlease enter your name: ").strip()
    print(f"Hello, {user_info['name']}! Let's get started.")
    
    load_expenses()
    
    while True:
        choice = display_menu()
        
        if choice == "1":
            modify_monthly_budget()
        elif choice == "2":
            add_expense()
        elif choice == "3":
            view_expenses()
        elif choice == "4":
            delete_expense()
        elif choice == "5":
            generate_report()
        elif choice == "6":
            if input("Are you sure you want to reset all data? (yes/no): ").strip().lower() == "yes":
                reset_data()
        elif choice == "7":
            print("Exiting...")
            save_expenses()
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__": 
    main()