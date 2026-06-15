from datetime import datetime

class Bank:
    withdraw_limit = 20000

    def __init__(self, name, account_number, address, balance, password):
        self.name = name
        self.account_number = account_number
        self.address = address
        self.balance = balance
        self.password = password
        self.transactions = []

    def credit(self, amount):
        while True:
            password = int(input("Enter your password: "))
            if password == self.password:
                self.balance += amount
                self.transactions.append((datetime.now(), 'Deposit\t',amount, self.balance))
                print(f"Your current balance is: {self.balance}")
                break
            else:
                print("Incorrect password! Try again.")

    def debit(self):
        while True:
            amount = int(input("Enter the amount to withdraw: "))
            if amount <= self.withdraw_limit:
                password = int(input("Enter your password: "))
                if password == self.password:
                    if self.balance >= amount:
                        self.balance -= amount
                        self.transactions.append((datetime.now(), 'Withdraw', amount, self.balance))
                        print(f"Withdrawal successful! Your current balance is: {self.balance}")
                        break
                    else:
                        print("Insufficient balance!")
                        break
                else:
                    print("Incorrect password! Try again.")
            else:
                print("Amount exceeds withdrawal limit. Please choose less than or equal to 20000.")

    def check_balance(self):
        while True:
            password = int(input("Enter your password: "))
            if password == self.password:
                print(f"Your current balance is: {self.balance}")
                break
            else:
                print("Incorrect password! Try again.")

    def mini_stat(self):
        while True:
            password = int(input("Enter your password: "))
            if password == self.password:
                print("\nMini Statement:")
                print("Date and Time\t\t\tTransaction Type\tAmount\tBalance")
                for transaction in self.transactions:
                    print(f"{transaction[0]}\t{transaction[1]}\t{transaction[2]}\t{transaction[3]}")
                break
            else:
                print("Incorrect password! Try again.")

    def del_acc(self, customers):
        while True:
            password = int(input("Enter your password: "))
            if password == self.password:
                customers.remove(self)
                print("Your account has been deleted.")
                break
            else:
                print("Incorrect password! Try again.")

    def money_transfer(self):
        y=True
        while y:
            c=int(input("receiver's account number"))
            password = int(input("enter password"))
            if password == self.password:
                customer=None
                for cust in customers:
                    if cust.account_number == c:
                        customer=cust
                        if customer :
                            cash=int(input("enter money to transfer"))
                            if cash <= self.balance:
                                self.balance -= cash
                                customer.balance += cash
                                self.transactions.append((datetime.now(), 'transferred',cash, self.balance))
                                customer.transactions.append((datetime.now(), 'received',cash, customer.balance))
                                print(f"transaction successful of amount {cash} to {customer.name}")
                                y=False

                            else :
                                print("insufficient balance! Try again")

                if customer == None:
                    print("user not found try again")
                    break
            else :
                print("Incorrect password! Try again.")





customers = []
customer1 = Bank("Ram", 1898013381, "Delhi", 500000, 2580)
customer2 = Bank("Sai", 1898013382, "Hyderabad", 200000, 1234)
customer3 = Bank("Dev", 1898013383, "Bangalore", 800000, 1111)

customers.append(customer1)
customers.append(customer2)
customers.append(customer3)
next_account_number = 1898013384

while True:
    choice = int(input("1: Create New Account\n2: Existing Account\n3: Exit\nEnter your choice: "))

    if choice == 1:
        name = input("Enter your name: ")
        address = input("Enter your address: ")
        balance = int(input("Enter initial deposit amount: "))
        password = int(input("Set your password (numeric): "))
        new_customer = Bank(name, next_account_number, address, balance, password)
        customers.append(new_customer)
        print(f"Account created successfully! Your account number is {next_account_number}")
        next_account_number += 1

    elif choice == 2:
        account_number = int(input("Enter your account number: "))
        customer=None
        for cust in customers:
            if cust.account_number==account_number:
                customer=cust

                if customer:
                    while True:
                        g = int(input("\n1: Deposit\n2: Withdraw\n3: Check Balance\n4: Mini Statement\n5: Delete account\n6: Customer details\n7: Exit to Main Menu\n8: Money Transfer\nEnter your choice: "))

                        if g == 1:
                            amount = int(input("Enter the amount to deposit: "))
                            customer.credit(amount)

                        elif g == 2:
                            customer.debit()

                        elif g == 3:
                            customer.check_balance()

                        elif g == 4:
                            customer.mini_stat()

                        elif g == 5:
                            customer.del_acc(customers)
                            break
                        elif g == 6:
                            print("account number\tname\tadddress")
                            print(f"{customer.account_number}\t\t{customer.name}\t\t{customer.address}")

                        elif g == 7:
                            break

                        elif g==8:
                            customer.money_transfer()


                        else:
                            print("Invalid choice! Please try again.")
        if customer == None:
            print("Account not found! Please try again.")

    elif choice == 3:
        print("Thank you for using our banking system. Goodbye!")
        break



    else:
        print("Invalid choice! Please try again.")

