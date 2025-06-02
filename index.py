from datetime import datetime

class Transaction:
    def __init__(self, amount, narration, transaction_type):
        self.date_time = datetime.now()
        self.amount = amount
        self.narration = narration
        self.transaction_type = transaction_type

    def __str__(self):
        return f"{self.date_time.strftime('%Y-%m-%d %H:%M:%S')} | {self.transaction_type} | {self.narration} | Amount: {self.amount}"


class Account:
    account_counter = 100000

    def __init__(self, owner, min_balance=0):
        self.owner = owner
        self.deposits = []
        self.withdrawals = []
        self.loan = 0
        self.__balance = 0
        self.frozen = False
        self.min_balance = min_balance
        self.closed = False
        self.transactions = []
        self.__account_number = Account.account_counter
        Account.account_counter += 1

    def get_balance(self):
        balance = 0
        for t in self.transactions:
            if t.transaction_type == "Deposit" or t.transaction_type == "Loan Credit":
                balance += t.amount
            elif t.transaction_type in ("Withdrawal", "Loan Repayment", "Transfer Out"):
                balance -= t.amount
        return balance

    def get_account_number(self):
        return self.__account_number

    def deposit(self, amount):
        if amount > 0 and not self.frozen and not self.closed:
            self.transactions.append(Transaction(amount, "Deposit to account", "Deposit"))
            return f"{self.owner}, you've deposited {amount}. Your new balance is {self.get_balance()}."
        return "Deposit failed. Amount must be positive and account must be active."

    def withdraw(self, amount):
        if self.frozen or self.closed:
            return "Account is not active."
        if amount > 0 and self.get_balance() - amount >= self.min_balance:
            self.transactions.append(Transaction(amount, "Withdrawal from account", "Withdrawal"))
            return f"Dear {self.owner}, you've withdrawn {amount}. Your new balance is {self.get_balance()}."
        return "Withdrawal failed. Insufficient balance or below minimum balance."

    def transfer_funds(self, amount, recipient_account):
        if self.frozen or self.closed:
            return "Account is not active."
        if amount > 0 and self.get_balance() - amount >= self.min_balance:
            self.transactions.append(Transaction(amount, f"Transfer to {recipient_account.owner}", "Transfer Out"))
            recipient_account.transactions.append(Transaction(amount, f"Transfer from {self.owner}", "Transfer In"))
            return f"You transferred {amount} to {recipient_account.owner}."
        return "Transfer failed due to insufficient funds or restrictions."

    def request_loan(self, amount):
        if amount > 0 and not self.frozen and not self.closed:
            self.loan += amount
            self.transactions.append(Transaction(amount, "Loan credited to account", "Loan Credit"))
            return f"Your loan request of {amount} approved. Your new balance is {self.get_balance()}."
        return "Your loan request failed."

    def repay_loan(self, amount):
        if amount > 0 and not self.frozen and not self.closed:
            if amount >= self.loan:
                repay_amount = self.loan
                self.loan = 0
                self.transactions.append(Transaction(repay_amount, "Full loan repayment", "Loan Repayment"))
                return "Your loan is fully repaid."
            else:
                self.loan -= amount
                self.transactions.append(Transaction(amount, "Partial loan repayment", "Loan Repayment"))
                return f"Partially repaid loan. Remaining loan balance is {self.loan}."
        return "Repayment failed."

    def view_account_details(self):
        return f"Owner: {self.owner}, Account Number: {self.get_account_number()}, Balance: {self.get_balance()}, Loan: {self.loan}"

    def change_account_owner(self, new_owner):
        if not self.closed:
            self.owner = new_owner
            return f"Account owner updated to {new_owner}."
        return "Cannot change owner of a closed account."

    def account_statement(self):
        print(f"Account Statement for {self.owner}")
        for t in self.transactions:
            print(t)
        print(f"Loan: {self.loan}")

    def calculate_interest(self):
        if not self.frozen and not self.closed:
            interest = self.get_balance() * 0.05
            self.transactions.append(Transaction(interest, "Interest credited", "Deposit"))
            return f"Interest of {interest} added. New balance: {self.get_balance()}."
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
        self.closed = True
        self.transactions.clear()
        self.loan = 0
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