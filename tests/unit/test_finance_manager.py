import pytest
from src.finance_manager import FinanceManager
from src.user import User
from src.transaction import Transaction

class TestFinanceManager:
    @pytest.fixture
    def manager():
        user = User("Alice", "alice@example.com", 25)
        return FinanceManager(user)

    # adding transactions to history
    def test_add_transaction_to_history(self, manager):
        t1 = Transaction(amount=100.0, category="Food")
        t2 = Transaction(amount=2000.0, category="Salary")
        
        manager.add_transaction(t1)
        manager.add_transaction(t2)
        
        assert len(manager.get_history()) == 2
        assert manager.get_history()[0].category == "Food"

    # calculating total balance
    def test_calculate_balance(self, manager):
        manager.add_transaction(Transaction(amount=1000.0, category="Salary")) # Income
        manager.add_transaction(Transaction(amount=200.0, category="Food"))    # Expense
        manager.add_transaction(Transaction(amount=50.0, category="Bus"))      # Expense
        
        # 1000 - 200 - 50 = 750
        assert manager.get_balance() == 750.0

    # budget limit warning (conditional logic)
    def test_budget_limit_warning(self, manager):
        manager.set_monthly_limit(500.0)
        manager.add_transaction(Transaction(amount=400.0, category="Rent"))
        
        # still under limit
        assert manager.check_budget_status() == "Within limit"
        
        # exceeding limit
        manager.add_transaction(Transaction(amount=200.0, category="Food"))
        assert manager.check_budget_status() == "Limit exceeded"

    # filtering history by type (Income/Expense)
    def test_filter_history_by_type(self, manager):
        manager.add_transaction(Transaction(amount=100.0, category="Food"))
        manager.add_transaction(Transaction(amount=500.0, category="Salary"))
        
        expenses = manager.get_filtered_history(transaction_type="Expense")
        assert len(expenses) == 1
        assert expenses[0].category == "Food"