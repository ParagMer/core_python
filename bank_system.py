import json
import os

# BankAccount class to represent a bank account
class BankAccount:
    def __init__(self, account_holder, balance=0):
        self.account_holder = account_holder
        self.balance = balance
        self.transaction_history = []
        
        # Load existing transaction history if it exists
        self.load_transaction_history()
    
    def load_transaction_history(self):
        """Load transaction history from a file."""
        try:
            if os.path.exists(f"{self.account_holder}_transactions.json"):
                with open(f"{self.account_holder}_transactions.json", "r") as file:
                    self.transaction_history = json.load(file)
        except Exception as e:
            print(f"Error loading transaction history: {e}")
    
    def save_transaction_history(self):
        """Save transaction history to a file."""
        try:
            with open(f"{self.account_holder}_transactions.json", "w") as file:
                json.dump(self.transaction_history, file, indent=4)
        except Exception as e:
            print(f"Error saving transaction history: {e}")
    
    def deposit(self, amount):
        """Deposit money into the account."""
        if amount <= 0:
            raise ValueError("Deposit amount must be greater than 0")
        self.balance += amount
        self.transaction_history.append(f"Deposited: {amount}")
        self.save_transaction_history()
    
    def withdraw(self, amount):
        """Withdraw money from the account."""
        if amount <= 0:
            raise ValueError("Withdrawal amount must be greater than 0")
        if amount > self.balance:
            raise ValueError("Insufficient balance")
        self.balance -= amount
        self.transaction_history.append(f"Withdrew: {amount}")
        self.save_transaction_history()
    
    def transfer(self, amount, target_account):
        """Transfer money to another account."""
        if amount <= 0:
            raise ValueError("Transfer amount must be greater than 0")
        if amount > self.balance:
            raise ValueError("Insufficient balance")
        self.balance -= amount
        target_account.balance += amount
        self.transaction_history.append(f"Transferred {amount} to {target_account.account_holder}")
        target_account.transaction_history.append(f"Received {amount} from {self.account_holder}")
        self.save_transaction_history()
        target_account.save_transaction_history()
    
    def get_balance(self):
        """Get the current balance."""
        return self.balance
    
    def generate_mini_statement(self):
        """Generate a mini-statement of recent transactions."""
        print(f"\nMini Statement for {self.account_holder}:")
        for transaction in self.transaction_history[-5:]:
            print(transaction)

# Inherited class for checking account
class CheckingAccount(BankAccount):
    def __init__(self, account_holder, balance=0):
        super().__init__(account_holder, balance)
        self.account_type = "Checking"
        
# Inherited class for savings account
class SavingsAccount(BankAccount):
    def __init__(self, account_holder, balance=0):
        super().__init__(account_holder, balance)
        self.account_type = "Savings"

# Main function to run the system
def run_bank_system():
    # Create a couple of accounts for demonstration
    user1 = CheckingAccount("Alice", 1000)
    user2 = SavingsAccount("Bob", 500)
    
    # Deposit money to Alice's account
    try:
        user1.deposit(200)
        print(f"Alice's balance: {user1.get_balance()}")
    except ValueError as e:
        print(e)
    
    # Withdraw money from Bob's account
    try:
        user2.withdraw(100)
        print(f"Bob's balance: {user2.get_balance()}")
    except ValueError as e:
        print(e)
    
    # Transfer money from Alice to Bob
    try:
        user1.transfer(150, user2)
        print(f"Alice's balance after transfer: {user1.get_balance()}")
        print(f"Bob's balance after transfer: {user2.get_balance()}")
    except ValueError as e:
        print(e)
    
    # Generate mini-statements
    user1.generate_mini_statement()
    user2.generate_mini_statement()

# Run the Bank System
if __name__ == "__main__":
    run_bank_system()
