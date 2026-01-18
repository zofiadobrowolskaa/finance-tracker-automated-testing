class FinanceManager:
    def __init__(self, user):
        self.user = user
        self.transactions = []
        self.monthly_limit = 0.0

    def add_transaction(self, transaction):
        # add transactions that have a valid amount
        if transaction.amount != "Invalid":
            self.transactions.append(transaction)
            return True
        return False

    def get_history(self):
        return self.transactions

    def get_balance(self):
        incomes = sum(t.amount for t in self.transactions if t.type == "Income")
        expenses = sum(t.amount for t in self.transactions if t.type == "Expense")
        return incomes - expenses

    def set_monthly_limit(self, limit):
        if isinstance(limit, (int, float)) and limit > 0:
            self.monthly_limit = limit
            return True
        return False

    def check_budget_status(self):
        if self.monthly_limit == 0:
            return "No limit set"
        
        total_expenses = sum(t.amount for t in self.transactions if t.type == "Expense")
        return "Limit exceeded" if total_expenses > self.monthly_limit else "Within limit"

    def get_filtered_history(self, transaction_type):
        return [t for t in self.transactions if t.type == transaction_type]