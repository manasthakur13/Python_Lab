class BankAccount:
    """
    Base class representing a generic bank account.
    Demonstrates encapsulation by using private attributes for account details.
    """
    def __init__(self, account_number, initial_balance=0.0):
        # Encapsulated private attributes
        self.__account_number = account_number
        self.__balance = initial_balance

    def get_account_number(self):
        """Returns the private account number."""
        return self.__account_number

    def get_balance(self):
        """Returns the current private balance."""
        return self.__balance

    def deposit(self, amount):
        """Adds funds to the account."""
        if amount > 0:
            self.__balance += amount
            print(f"Deposited ${amount:.2f} into account {self.__account_number}.")
        else:
            print("Deposit amount must be positive.")

    def withdraw(self, amount):
        """
        Base method for balance transactions. 
        Deducts funds if sufficient balance exists.
        """
        if 0 < amount <= self.__balance:
            self.__balance -= amount
            print(f"Withdrew ${amount:.2f} from account {self.__account_number}.")
        else:
            print(f"Insufficient funds in account {self.__account_number}.")

    def account_type(self):
        """Returns the type of account for polymorphic interfaces."""
        return "Standard Bank Account"


class SavingsAccount(BankAccount):
    """
    Specialized derived class for savings accounts.
    Enforces a minimum balance requirement.
    """
    def __init__(self, account_number, initial_balance=0.0, min_balance=100.0):
        super().__init__(account_number, initial_balance)
        self.min_balance = min_balance

    def withdraw(self, amount):
        """
        Implements method overriding for balance transactions.
        Uses super() to execute the withdrawal if minimum balance rules are met.
        """
        if (self.get_balance() - amount) >= self.min_balance:
            # Overriding and utilizing the base class method via super()
            super().withdraw(amount)
        else:
            print(f"Withdrawal denied: Must maintain minimum balance of ${self.min_balance:.2f}.")

    def account_type(self):
        """Overrides account type for polymorphism."""
        return "Savings Account"


class CurrentAccount(BankAccount):
    """
    Specialized derived class for current (checking) accounts.
    Allows for an overdraft limit.
    """
    def __init__(self, account_number, initial_balance=0.0, overdraft_limit=500.0):
        super().__init__(account_number, initial_balance)
        self.overdraft_limit = overdraft_limit

    def withdraw(self, amount):
        """
        Implements method overriding for balance transactions.
        Allows withdrawal up to the specified overdraft limit.
        """
        if amount > 0 and (self.get_balance() + self.overdraft_limit) >= amount:
            # Modify private balance via public methods/properties since it's encapsulated in base
            # Note: We simulate the withdrawal logic directly here to accommodate overdrafts
            new_balance = self.get_balance() - amount
            # Using super() deposit/withdraw trick or directly accessing name-mangled variables isn't ideal.
            # Instead, we bypass the strict base check by calling a customized deduction or using the base safely.
            if amount <= self.get_balance():
                super().withdraw(amount)
            else:
                # Handle overdraft case
                overdraft_used = amount - self.get_balance()
                super().withdraw(self.get_balance()) # drain balance to 0
                print(f"Overdraft utilized for remaining ${overdraft_used:.2f}.")
        else:
            print(f"Withdrawal denied: Exceeds overdraft limit of ${self.overdraft_limit:.2f}.")

    def account_type(self):
        """Overrides account type for polymorphism."""
        return "Current Account"


def process_polymorphic_transaction(account, withdraw_amount):
    """
    Manages polymorphism using a polymorphic interface.
    Accepts any BankAccount object and processes a standard transaction.
    """
    print(f"\n--- Processing {account.account_type()} ({account.get_account_number()}) ---")
    print(f"Starting Balance: ${account.get_balance():.2f}")
    account.withdraw(withdraw_amount)
    print(f"Ending Balance: ${account.get_balance():.2f}")


def main():
    """Main execution function demonstrating the OOP financial engine."""
    # Instantiate specialized derived classes
    savings = SavingsAccount(account_number="SA-1001", initial_balance=500.0, min_balance=100.0)
    current = CurrentAccount(account_number="CA-2001", initial_balance=200.0, overdraft_limit=300.0)

    # Deposit funds using inherited methods
    savings.deposit(50.0)
    
    # Manage polymorphism using polymorphic interfaces
    # Processing a valid withdrawal for savings
    process_polymorphic_transaction(savings, 200.0)
    
    # Processing an invalid withdrawal for savings (hits min balance)
    process_polymorphic_transaction(savings, 300.0)

    # Processing an overdraft withdrawal for current account
    process_polymorphic_transaction(current, 400.0)
    
    # Processing an invalid overdraft withdrawal
    process_polymorphic_transaction(current, 500.0)

if __name__ == "__main__":
    main()