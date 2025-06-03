import csv
import pandas as pd
from datetime import datetime

class ExpenseTracker:
    def __init__(self, filename="expenses.csv"):
        self.filename = filename
        self.ensure_file_exists()

    def ensure_file_exists(self):
        """Ensure the CSV file exists, otherwise create one with headers."""
        try:
            with open(self.filename, mode='r') as file:
                pass
        except FileNotFoundError:
            with open(self.filename, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['Date', 'Category', 'Amount', 'Description'])

    def add_expense(self, category, amount, description):
        """Add a new expense record."""
        date = datetime.now().strftime("%Y-%m-%d")
        with open(self.filename, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([date, category, amount, description])
        print(f"Expense added for {category} on {date}")

    def generate_monthly_report(self, month, year):
        """Generate a monthly expense report."""
        expenses = pd.read_csv(self.filename)
        expenses['Date'] = pd.to_datetime(expenses['Date'])
        monthly_expenses = expenses[(expenses['Date'].dt.month == month) & (expenses['Date'].dt.year == year)]
        
        if monthly_expenses.empty:
            print(f"No expenses recorded for {datetime(year, month, 1).strftime('%B %Y')}")
            return

        total_expenses = monthly_expenses['Amount'].sum()
        print(f"\n--- Monthly Report for {datetime(year, month, 1).strftime('%B %Y')} ---")
        print(f"Total Expenses: {total_expenses:.2f}")
        print("Details:")
        print(monthly_expenses)
        
        return monthly_expenses

    def filter_expenses(self, category=None, min_amount=None, max_amount=None):
        """Filter expenses based on category or amount range."""
        expenses = pd.read_csv(self.filename)
        
        if category:
            expenses = expenses[expenses['Category'].str.lower() == category.lower()]
        if min_amount is not None:
            expenses = expenses[expenses['Amount'] >= min_amount]
        if max_amount is not None:
            expenses = expenses[expenses['Amount'] <= max_amount]
        
        print("\n--- Filtered Expenses ---")
        print(expenses)
        return expenses

    def sort_expenses(self, by_column='Date'):
        """Sort expenses by a specified column."""
        expenses = pd.read_csv(self.filename)
        sorted_expenses = expenses.sort_values(by=by_column, ascending=False)
        
        print(f"\n--- Sorted Expenses by {by_column} ---")
        print(sorted_expenses)
        return sorted_expenses

# Main Program
def main():
    tracker = ExpenseTracker()

    while True:
        print("\n--- Expense Tracker ---")
        print("1. Add Expense")
        print("2. Generate Monthly Report")
        print("3. Filter Expenses")
        print("4. Sort Expenses")
        print("5. Exit")

        try:
            choice = int(input("Enter your choice: "))
            if choice == 1:
                category = input("Enter expense category (e.g., Food, Transport): ")
                amount = float(input("Enter expense amount: "))
                description = input("Enter description: ")
                tracker.add_expense(category, amount, description)

            elif choice == 2:
                month = int(input("Enter month (1-12): "))
                year = int(input("Enter year (e.g., 2025): "))
                tracker.generate_monthly_report(month, year)

            elif choice == 3:
                print("\nFilter Options:")
                category = input("Enter category to filter by (leave blank for all): ")
                min_amount = input("Enter minimum amount (leave blank for no minimum): ")
                max_amount = input("Enter maximum amount (leave blank for no maximum): ")

                min_amount = float(min_amount) if min_amount else None
                max_amount = float(max_amount) if max_amount else None
                tracker.filter_expenses(category, min_amount, max_amount)

            elif choice == 4:
                by_column = input("Enter column to sort by (Date, Category, Amount): ")
                tracker.sort_expenses(by_column)

            elif choice == 5:
                print("Exiting the system...")
                break
            else:
                print("Invalid choice, please try again.")
        except ValueError:
            print("Please enter a valid number.")

if __name__ == "__main__":
    main()
