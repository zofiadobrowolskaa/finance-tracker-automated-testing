import datetime

class Transaction:
    # business logic: predefined income categories
    INCOME_CATEGORIES = ["Salary", "Bonus", "Gift", "Interest"]

    def __init__(self, amount, category, date=None):
        self.amount = self.is_amount_valid(amount)
        self.category = category
        self.date = date if date else datetime.date.today().strftime("%Y-%m-%d")
        self.type = self.assign_type(category)
        
        # external functionality placeholder (to be mocked later)
        from src.utils.id_generator import generate_transaction_id
        self.transaction_id = generate_transaction_id()

    def is_amount_valid(self, amount):
        if isinstance(amount, (int, float)) and amount > 0:
            return amount
        return "Invalid"

    def assign_type(self, category):
        return "Income" if category in self.INCOME_CATEGORIES else "Expense"