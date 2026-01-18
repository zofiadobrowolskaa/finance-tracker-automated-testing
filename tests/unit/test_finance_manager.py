import pytest
from src.finance_manager import FinanceManager
from src.user import User
from src.transaction import Transaction

class TestFinanceManager:
    @pytest.fixture
    def manager(self):
        user = User("Alice", "alice@example.com", 25)
        return FinanceManager(user)

    # adding transactions to history
    def test_add_transaction_to_history(self, manager):
        manager.add_transaction(Transaction(amount=100.0, category="Food"))
        manager.add_transaction(Transaction(amount=2000.0, category="Salary"))
        
        assert len(manager.get_history()) == 2
        assert manager.get_history()[0].category == "Food"

    # calculating total balance (Incomes - Expenses)
    def test_calculate_balance(self, manager):
        manager.add_transaction(Transaction(amount=1000.0, category="Salary"))
        manager.add_transaction(Transaction(amount=200.0, category="Food"))
        assert manager.get_balance() == 800.0

    # parametrization: test various budget limit scenarios and expected status messages
    @pytest.mark.parametrize("limit, expense_amount, expected_status", [
        (0.0, 100.0, "No limit set"),
        (500.0, 400.0, "Within limit"),
        (500.0, 600.0, "Limit exceeded"),
    ])
    def test_budget_status_scenarios(self, manager, limit, expense_amount, expected_status):
        manager.set_monthly_limit(limit)
        manager.add_transaction(Transaction(amount=expense_amount, category="General"))
        assert manager.check_budget_status() == expected_status

    # filtering history by type (Income/Expense)
    def test_filter_history_by_type(self, manager):
        manager.add_transaction(Transaction(amount=100.0, category="Food"))
        manager.add_transaction(Transaction(amount=500.0, category="Salary"))
        
        expenses = manager.get_filtered_history("Expense")
        assert all(t.type == "Expense" for t in expenses)
        assert len(expenses) == 1