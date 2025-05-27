# class Account:
#     def __init__(self, name):
#         self.name = name
#         self.deposits = []
#         self.withdrawals = []
#         self.transfers = []
#         self.loans = []
#         self.loan_repayments = []
#         self.balance = 0
#         self.frozen = False
#         self.min_balance = 0
#         self.closed = False

#     def deposit(self, amount):
#         if amount <= 0:
#             return "The deposited amount is invalid"
#         if amount>0:
#         self.deposits.append(amount)
#         self.balance += amount
#         return f"{amount} deposited successfully. Your new balance is {self.balance}"

#     def withdraw(self, amount):
#         if amount <= 0:
#             return "You can't withdraw a negative amount."
#         if self.balance - amount < self.min_balance:
#             return "Insufficient balance or minimum balance restriction."
#         self.withdrawals.append(amount)
#         self.balance -= amount
#         return f"{amount} withdrawn successfully. New balance: {self.balance}"

#     def transfer(self, amount, user_account):    
#         if amount <= 0:
#             return "You can't transfer a negative amount."
#         if self.balance - amount < self.min_balance:
#             return "Insufficient funds or minimum balance restriction."
#         self.transfers.append(amount)
#         self.balance -= amount
#         user_account.deposit(amount)
#         return f"{amount} transferred to {user_account.name}. New balance: {self.balance}"

#     def get_balance(self):
#         return f"Your current balance is {self.balance}"
        
#     def request_loan(self, amount):
#         if amount <= 0:
#             return "Invalid loan amount"
#         self.loans.append(amount)
#         self.balance += amount
#         return f"Loan of {amount} approved. New balance: {self.balance}"

#     def repay_loan(self, amount):
#         if amount <= 0:
#             return "You can't repay a negative amount."
#         if sum(self.loans) == 0:
#             return "You have no loans."
#         self.loan_repayments.append(amount)
#         self.balance -= amount
#         return f"You paid {amount} successful. Your remaining loan: {sum(self.loans) - sum(self.loan_repayments)}"

#     def view_account_details(self):
#         return f"Account
#         for t in self.transfers:
#             print(f" -{t}")
#         print(f"Current Balance: {self.balance}")

#     def get_loan_statement(self):
#         print(f"Loan Statement of {self.name}")
#         print("Taken Loans:")
#         for loan in self.loans:
#             print(f" +{loan}")
#         print("Loan Repayments:")
#         for repayment in self.loan_repayments:
#             print(f" -{repayment}")
#         print(f"Remaining Loan: {sum(self.loans) - sum(self.loan_repayments)}")

#     def apply_interest(self):
#         interest = self.balance * 0.05
#         self.balance += interest
#         return f"Interest of {interest} applied. New balance: {self.balance}"

#     def freeze_account(self):
#         self.frozen = True
#         return "Account has been frozen."

#     def unfreeze_account(self):
#         self.frozen = False
#         return "Account has been unfrozen."

#     def set_min_balance(self, amount):
#         if amount < 0:
#             return "Minimum balance cannot be negative."
#         self.min_balance = amount
#         return f"Minimum balance set to {amount}."

#     def close_account(self):
#         self.closed = True
#         self.deposits.clear()
#         self.withdrawals.clear()
#         self.transfers.clear()
#         self.loans.clear()
#         self.loan_repayments.clear()
#         self.balance = 0
#         return "Account has been closed."


class Account:
    def __init__(self, owner, min_balance=0):
        self.owner = owner
        self.deposits = []
        self.withdrawals = []
        self.loan = 0
        self.balance = 0
        self.frozen = False
        self.min_balance = min_balance
        self.closed = False

    def deposit(self, amount):
        if amount > 0 and not self.frozen and not self.closed:
            self.deposits.append(amount)
            self.balance += amount
            return f"{self.owner}, you've deposited {amount}. New balance is {self.balance}."
        return "Deposit failed. Amount must be positive and account must be active."

    def withdraw(self, amount):
        if self.frozen or self.closed:
            return "Account is not active."
        if amount > 0 and self.balance - amount >= self.min_balance:
            self.withdrawals.append(amount)
            self.balance -= amount
            return f"{self.owner}, you've withdrawn {amount}. New balance is {self.balance}."
        return "Withdrawal failed. Insufficient balance or below minimum balance."

    def transfer_funds(self, amount, recipient_account):
        if self.frozen or self.closed:
            return "Account is not active."
        if amount > 0 and self.balance - amount >= self.min_balance:
            self.withdraw(amount)
            recipient_account.deposit(amount)
            return f"Transferred {amount} to {recipient_account.owner}."
        return "Transfer failed due to insufficient funds or restrictions."

    def get_balance(self):
        return self.balance

    def request_loan(self, amount):
        if amount > 0 and not self.frozen and not self.closed:
            self.loan += amount
            self.balance += amount
            return f"Loan of {amount} approved. New balance is {self.balance}."
        return "Loan request failed."

    def repay_loan(self, amount):
        if amount > 0 and not self.frozen and not self.closed:
            if amount >= self.loan:
                self.balance -= self.loan
                self.loan = 0
                return "Loan fully repaid."
            else:
                self.loan -= amount
                self.balance -= amount
                return f"Partially repaid loan. Remaining loan balance is {self.loan}."
        return "Repayment failed."

    def view_account_details(self):
        return f"Owner: {self.owner}, Balance: {self.balance}, Loan: {self.loan}"

    def change_account_owner(self, new_owner):
        if not self.closed:
            self.owner = new_owner
            return f"Account owner updated to {new_owner}."
        return "Cannot change owner of a closed account."

    def account_statement(self):
        print(f"Account Statement for {self.owner}")
        for d in self.deposits:
            print(f"Deposit: {d}")
        for w in self.withdrawals:
            print(f"Withdrawal: {w}")
        print(f"Loan: {self.loan}")

    def calculate_interest(self):
        if not self.frozen and not self.closed:
            interest = self.balance * 0.05
            self.balance += interest
            return f"Interest of {interest} added. New balance: {self.balance}."
        return "Interest not applied. Account must be active."

    def freeze_account(self):
        self.frozen = True
        return "Account has been frozen."

    def unfreeze_account(self):
        self.frozen = False
        return "Account has been unfrozen."

    def set_minimum_balance(self, amount):
        self.min_balance = amount
        return f"Minimum balance set to {amount}."

    def close_account(self):
        self.balance = 0
        self.deposits.clear()
        self.withdrawals.clear()
        self.loan = 0
        self.closed = True
        return "Account has been closed."



tirsit = Account(owner="Tirsit", min_balance=100)
amanuel = Account(owner="Amanuel")


print(tirsit.deposit(500))  
print(tirsit.withdraw(200)) 
print(tirsit.withdraw(250)) 
print(tirsit.transfer_funds(100, amanuel))  
print(f"Tirsit's balance: {tirsit.get_balance()}")  
print(f"Amanuel's balance: {amanuel.get_balance()}")   
print(tirsit.request_loan(300)) 
print(tirsit.repay_loan(100))   
print(tirsit.repay_loan(200))  
print(tirsit.view_account_details()) 
print(tirsit.change_account_owner("Meron"))  
print(tirsit.freeze_account())          
print(tirsit.deposit(50))              
print(tirsit.unfreeze_account())          
print(tirsit.deposit(50))                
print(tirsit.calculate_interest())       
tirsit.account_statement()
print(tirsit.close_account())            
print(tirsit.deposit(100))               