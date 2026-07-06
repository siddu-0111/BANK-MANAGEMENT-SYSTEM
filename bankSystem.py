import os
import random
from datetime import datetime

# Files used to store data permanently
CUSTOMERS_FILE = "customers.txt"
TRANSACTIONS_FILE = "transactions.txt"


class Bank:
    withdraw_limit = 20000

    def __init__(self, name, account_number, address, balance, password):
        self.name = name
        self.account_number = account_number
        self.address = address
        self.balance = balance
        self.password = password
        self.transactions = []

    def credit(self):
        done = False
        while not done:
            amount = int(input("Enter the amount to deposit: "))
            if amount <= 0:
                print("Amount must be greater than zero. Please try again.")
            else:
                password = int(input("Enter your password: "))
                if password == self.password:
                    self.balance += amount
                    self.transactions.append((datetime.now(), 'Deposit\t', amount, self.balance))
                    save_customers(customers)  # update customers.txt with new balance
                    log_transaction(self.account_number, self.name, "Deposit", amount, self.balance)
                    print(f"Your current balance is: {self.balance}")
                    done = True
                else:
                    print("Incorrect password! Try again.")

    def debit(self):
        done = False
        while not done:
            amount = int(input("Enter the amount to withdraw: "))
            if amount <= 0:
                print("Amount must be greater than zero. Please try again.")
            elif amount <= self.withdraw_limit:
                password = int(input("Enter your password: "))
                if password == self.password:
                    if self.balance >= amount:
                        self.balance -= amount
                        self.transactions.append((datetime.now(), 'Withdraw', amount, self.balance))
                        save_customers(customers)  # update customers.txt with new balance
                        log_transaction(self.account_number, self.name, "Withdraw", amount, self.balance)
                        print(f"Withdrawal successful! Your current balance is: {self.balance}")
                        done = True
                    else:
                        print("Insufficient balance!")
                        done = True
                else:
                    print("Incorrect password! Try again.")
            else:
                print("Amount exceeds withdrawal limit. Please choose less than or equal to 20000.")

    def check_balance(self):
        done = False
        while not done:
            password = int(input("Enter your password: "))
            if password == self.password:
                print(f"Your current balance is: {self.balance}")
                done = True
            else:
                print("Incorrect password! Try again.")

    def mini_stat(self):
        done = False
        while not done:
            password = int(input("Enter your password: "))
            if password == self.password:
                print("\nMini Statement:")
                print(f"{'Date & Time':<24}{'Account No':<16}{'Name':<12}{'Transaction':<17}{'Amount':<12}{'Balance'}")
                print("-" * 90)
                # Read transactions.txt and print only this customer's rows
                if os.path.exists(TRANSACTIONS_FILE):
                    with open(TRANSACTIONS_FILE, "r") as f:
                        lines = f.readlines()
                    for line in lines[2:]:  # skip header and separator line
                        if str(self.account_number) in line:
                            print(line.rstrip())
                done = True
            else:
                print("Incorrect password! Try again.")

    def del_acc(self, customers):
        done = False
        while not done:
            password = int(input("Enter your password: "))
            if password == self.password:
                customers.remove(self)
                save_customers(customers)  # remove this account from customers.txt
                print("Your account has been deleted.")
                done = True
            else:
                print("Incorrect password! Try again.")

    def money_transfer(self):
        y = True
        while y:
            c = int(input("receiver's account number :"))
            password = int(input("enter password :"))
            if password == self.password:
                customer = None
                for cust in customers:
                    if cust.account_number == c:
                        customer = cust
                        if(customer.account_number == self.account_number):
                            print("You cannot transfer money to your own account. Please try again.")
                        else:
                            if customer:
                                cash = int(input("enter money to transfer"))
                                if cash <= 0:
                                    print("Amount must be greater than zero. Please try again.")
                                elif cash <= self.balance:
                                    self.balance -= cash
                                    customer.balance += cash
                                    self.transactions.append((datetime.now(), 'transferred', cash, self.balance))
                                    customer.transactions.append((datetime.now(), 'received', cash, customer.balance))
                                    save_customers(customers)  # update both balances on disk
                                    log_transaction(self.account_number, self.name, "Transfer", cash, self.balance)
                                    log_transaction(customer.account_number, customer.name, "Received", cash, customer.balance)
                                    print(f"transaction successful of amount {cash} to {customer.name}")
                                    y = False
                                else:
                                    print("insufficient balance! Try again")
                if customer is None:
                    print("user not found try again")
                    break
            else:
                print("Incorrect password! Try again.")


# ---------- File handling helper functions ----------

def load_customers():
    """Read customers.txt and return a list of Bank objects.
    If the file doesn't exist, create an empty one with just the header."""
    customers_list = []

    if not os.path.exists(CUSTOMERS_FILE):
        save_customers(customers_list)  # creates the file with header only
        return customers_list

    with open(CUSTOMERS_FILE, "r") as f:
        lines = f.readlines()

    for line in lines[2:]:  # skip header and separator line
        if line.strip() == "":
            continue
        parts = line.split()
        name, acc_no, address, balance, password = parts[0], parts[1], parts[2], parts[3], parts[4]
        customers_list.append(Bank(name, int(acc_no), address, int(balance), int(password)))

    return customers_list


def save_customers(customers_list):
    """Rewrite customers.txt with the current data of every customer."""
    with open(CUSTOMERS_FILE, "w") as f:
        f.write(f"{'Name':<15}{'Account No':<16}{'Address':<20}{'Balance':<13}{'Password'}\n")
        f.write("-" * 75 + "\n")
        for cust in customers_list:
            f.write(f"{cust.name:<15}{cust.account_number:<16}{cust.address:<20}{cust.balance:<13}{cust.password}\n")


def log_transaction(account_number, name, ttype, amount, balance):
    """Add one line to transactions.txt for every deposit, withdraw or transfer."""
    file_exists = os.path.exists(TRANSACTIONS_FILE)
    with open(TRANSACTIONS_FILE, "a") as f:
        if not file_exists:
            f.write(f"{'Date & Time':<24}{'Account No':<16}{'Name':<12}{'Transaction':<17}{'Amount':<12}{'Balance'}\n")
            f.write("-" * 90 + "\n")
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"{timestamp:<24}{account_number:<16}{name:<12}{ttype:<17}{amount:<12}{balance}\n")


def generate_account_number(customers_list):
    """Generate a random 10-digit account number that no existing customer has."""
    existing_numbers = [cust.account_number for cust in customers_list]
    acc_no = random.randint(1000000000, 9999999999)  # 10-digit number
    unique = acc_no not in existing_numbers
    while not unique:
        acc_no = random.randint(1000000000, 9999999999)
        unique = acc_no not in existing_numbers
    return acc_no


# ---------- Program start ----------

customers = load_customers()  # load saved customers instead of hard-coding them

running = True
while running:
    choice = int(input("1: Create New Account\n2: Existing Account\n3: Exit\nEnter your choice: "))

    if choice == 1:
        name = input("Enter your name: ")
        address = input("Enter your address: ")
        balance = int(input("Enter initial deposit amount: "))
        password = int(input("Set your password (numeric): "))
        new_account_number = generate_account_number(customers)  # unique 10-digit number
        new_customer = Bank(name, new_account_number, address, balance, password)
        customers.append(new_customer)
        save_customers(customers)  # save the new account right away
        print(f"Account created successfully! Your account number is {new_account_number}")

    elif choice == 2:
        account_number = int(input("Enter your account number: "))
        customer = None
        for cust in customers:
            if cust.account_number == account_number:
                customer = cust

                if customer:
                    browsing = True
                    while browsing:
                        g = int(input("\n1: Deposit\n2: Withdraw\n3: Check Balance\n4: Mini Statement\n5: Delete account\n6: Customer details\n7: Exit to Main Menu\n8: Money Transfer\nEnter your choice: "))

                        if g == 1:
                            customer.credit()

                        elif g == 2:
                            customer.debit()

                        elif g == 3:
                            customer.check_balance()

                        elif g == 4:
                            customer.mini_stat()

                        elif g == 5:
                            customer.del_acc(customers)
                            browsing = False
                        elif g == 6:
                            print("account number\tname\tadddress")
                            print(f"{customer.account_number}\t\t{customer.name}\t\t{customer.address}")

                        elif g == 7:
                            browsing = False

                        elif g == 8:
                            customer.money_transfer()

                        else:
                            print("Invalid choice! Please try again.")
        if customer is None:
            print("Account not found! Please try again.")

    elif choice == 3:
        print("Thank you for using our banking system. Goodbye!")
        running = False

    else:
        print("Invalid choice! Please try again.")