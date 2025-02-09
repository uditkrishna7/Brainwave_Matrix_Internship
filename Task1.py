class ATM:
    def __init__(self, initial_balance=0):
        """Initialize the ATM with an optional starting balance."""
        self.balance = initial_balance
        self.pin = None

    def create_pin(self):
        """Allow the user to set a PIN for the ATM account."""
        while True:
            pin = input("Create a 4-digit PIN: ")
            if pin.isdigit() and len(pin) == 4:
                self.pin = pin
                return "PIN created successfully!"
            else:
                print("Invalid PIN. Please enter a 4-digit number.")

    def validate_pin(self):
        """Validate the user's PIN before allowing access."""
        for _ in range(3):  # Allow 3 attempts
            pin = input("Enter your 4-digit PIN: ")
            if pin == self.pin:
                return True
            else:
                print("Incorrect PIN. Try again.")
        return False

    def change_pin(self):
        """Allow the user to change their PIN after validation."""
        if self.validate_pin():
            while True:
                new_pin = input("Enter a new 4-digit PIN: ")
                if new_pin.isdigit() and len(new_pin) == 4:
                    self.pin = new_pin
                    return "PIN changed successfully!"
                else:
                    print("Invalid PIN. Please enter a 4-digit number.")
        else:
            return "Failed to validate PIN. PIN change aborted."

    def check_balance(self):
        """Return the current balance."""
        return f"Your current balance is: ${self.balance:.2f}"

    def deposit(self, amount):
        """Add the specified amount to the balance."""
        if amount > 0:
            self.balance += amount
            return f"Deposited ${amount:.2f}. New balance: ${self.balance:.2f}"
        return "Deposit amount must be positive."

    def withdraw(self, amount):
        """Subtract the specified amount from the balance if sufficient funds are available."""
        if amount > 0:
            if amount <= self.balance:
                self.balance -= amount
                return f"Withdrew ${amount:.2f}. Remaining balance: ${self.balance:.2f}"
            return "Insufficient funds for this withdrawal."
        return "Withdrawal amount must be positive."

    def perform_action(self, action):
        """Execute an action based on the user's choice."""
        if action == 1:
            return self.check_balance()
        elif action == 2:
            amount = float(input("Enter the amount to deposit: "))
            return self.deposit(amount)
        elif action == 3:
            amount = float(input("Enter the amount to withdraw: "))
            return self.withdraw(amount)
        elif action == 4:
            return self.change_pin()
        elif action == 5:
            return "Exiting the ATM. Thank you!"
        return "Invalid action. Please choose a valid option."

# Main program loop
atm = ATM(initial_balance=1000)

print("Welcome to the ATM System")

# Set up PIN if not already created
if not atm.pin:
    print(atm.create_pin())

# Validate PIN before accessing options
if atm.validate_pin():
    while True:
        print("\nMenu")
        print("1. Check Balance")
        print("2. Deposit Money")
        print("3. Withdraw Money")
        print("4. Change PIN")
        print("5. Exit")

        try:
            action = int(input("Please select an option (1-5): "))
            result = atm.perform_action(action)
            print(result)
            if action == 5:
                break
        except ValueError:
            print("Invalid input. Please enter a number between 1 and 5.")
else:
    print("Access denied. Too many incorrect PIN attempts.")
