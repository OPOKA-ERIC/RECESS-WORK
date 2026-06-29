"""
Lab 1 Exercise 1: Banking System
Demonstrates Method Overloading and Overriding
Author: Opoka Eric
Registration: U/24/10784/EVE
Student Number: 2400710784
"""

import abc

class Transaction(abc.ABC):
    def __init__(self, account_holder, account_number, balance=0.0):
        self.account_holder = account_holder
        self.account_number = account_number
        self._balance = balance

    # Method overloading simulation using default parameters
    def process(self, amount=0.0, description="No description"):
        print(f"[Transaction] Processing {description} for {self.account_holder}")
        return amount

    @abc.abstractmethod
    def get_transaction_type(self):
        pass

    def get_balance(self):
        return self._balance

    def display_info(self):
        print(f"Account Holder: {self.account_holder}")
        print(f"Account Number: {self.account_number}")
        print(f"Balance: ${self._balance:.2f}")

    @staticmethod
    def validate_amount(amount):
        if amount <= 0:
            raise ValueError("Amount must be positive")

    @staticmethod
    def validate_balance(balance, amount):
        if balance < amount:
            raise ValueError("Insufficient balance")


class Deposit(Transaction):
    def __init__(self, account_holder, account_number, balance=0.0):
        super().__init__(account_holder, account_number, balance)

    def get_transaction_type(self):
        return "DEPOSIT"

    # Overriding process method
    def process(self, amount=0.0, description="Deposit"):
        Transaction.validate_amount(amount)
        self._balance += amount
        print(f"[Deposit] ${amount:.2f} deposited. {description}")
        return self._balance


class Withdrawal(Transaction):
    def __init__(self, account_holder, account_number, balance=0.0):
        super().__init__(account_holder, account_number, balance)

    def get_transaction_type(self):
        return "WITHDRAWAL"

    # Overriding process method
    def process(self, amount=0.0, description="Withdrawal"):
        Transaction.validate_amount(amount)
        Transaction.validate_balance(self._balance, amount)
        self._balance -= amount
        print(f"[Withdrawal] ${amount:.2f} withdrawn. {description}")
        return self._balance


class Transfer(Transaction):
    def __init__(self, account_holder, account_number, balance=0.0):
        super().__init__(account_holder, account_number, balance)
        self.transfer_history = []

    def get_transaction_type(self):
        return "TRANSFER"

    # Overriding process method
    def process(self, amount=0.0, description="Transfer", recipient=None):
        Transaction.validate_amount(amount)
        Transaction.validate_balance(self._balance, amount)
        self._balance -= amount
        self.transfer_history.append({
            "recipient": recipient,
            "amount": amount,
            "description": description
        })
        print(f"[Transfer] ${amount:.2f} transferred to {recipient}. {description}")
        return self._balance

    # Additional overloaded method with different signature
    def process(self, amount=0.0, description="Transfer"):
        Transaction.validate_amount(amount)
        Transaction.validate_balance(self._balance, amount)
        self._balance -= amount
        print(f"[Transfer] ${amount:.2f} transferred. {description}")
        return self._balance


# Demonstration
if __name__ == "__main__":
    print("=" * 60)
    print("BANKING SYSTEM DEMONSTRATION")
    print("Author: Opoka Eric | U/24/10784/EVE | 2400710784")
    print("=" * 60)

    print("\n--- Creating Employer Account ---")
    employer = Deposit("Employer Corp", "ACC-001", 10000.0)
    employer.display_info()

    print("\n--- Depositing Salary ---")
    employer.process(5000.0, "Monthly salary deposit")
    print(f"New Balance: ${employer.get_balance():.2f}")

    print("\n--- Employer Withdraws Funds ---")
    withdraw_acc = Withdrawal("Employer Corp", "ACC-001", employer.get_balance())
    withdraw_acc.process(2000.0, "Office supplies purchase")
    print(f"New Balance: ${withdraw_acc.get_balance():.2f}")

    print("\n--- Employer Transfers to Vendor ---")
    transfer_acc = Transfer("Employer Corp", "ACC-001", withdraw_acc.get_balance())
    transfer_acc.process(1500.0, "Vendor payment for services", recipient="Vendor XYZ")
    print(f"New Balance: ${transfer_acc.get_balance():.2f}")

    print("\n--- Final Account Summary ---")
    transfer_acc.display_info()

    print("\n--- Method Overloading Example ---")
    t = Transaction("Test User", "ACC-000")
    t.process()
    t.process(100.0)
    t.process(200.0, "Overloaded method example")

    print("\n--- Method Overriding Example ---")
    transactions = [
        Deposit("User A", "ACC-002", 1000),
        Withdrawal("User A", "ACC-002", 1000),
        Transfer("User A", "ACC-002", 1000)
    ]
    for tx in transactions:
        print(f"\nProcessing {tx.get_transaction_type()}...")
        if isinstance(tx, Transfer):
            tx.process(100.0, "Sample transfer", recipient="User B")
        else:
            tx.process(100.0, "Sample transaction")
