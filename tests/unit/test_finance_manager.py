import pytest
from unittest.mock import patch
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

    # parametrization: test currency conversion for valid rates and error handling
    @pytest.mark.parametrize("currency, mock_rate, expected_result", [
        ("USD", 4.0, 25.0),
        ("EUR", 2.0, 50.0),
        ("GBP", None, None)
    ])
    # getting balance in different currency (mocked exchange rate)
    @patch('src.utils.currency_service.CurrencyService.get_exchange_rate')
    def test_get_balance_in_currency_scenarios(self, mock_get_rate, manager, currency, mock_rate, expected_result):
        manager.add_transaction(Transaction(amount=100.0, category="Gift"))

        mock_get_rate.return_value = mock_rate
        
        result = manager.get_balance_in_currency(currency)
        assert result == expected_result
        
        mock_get_rate.assert_called_with(currency)

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

    # parametrization: ensure filtering works for both Incomes and Expenses
    @pytest.mark.parametrize("filter_type, expected_count", [
        ("Expense", 1),
        ("Income", 1)
    ])
    def test_filter_history_scenarios(self, manager, filter_type, expected_count):
        manager.add_transaction(Transaction(amount=100.0, category="Food"))
        manager.add_transaction(Transaction(amount=500.0, category="Salary"))
        
        filtered = manager.get_filtered_history(filter_type)
        assert len(filtered) == expected_count
        assert all(t.type == filter_type for t in filtered)