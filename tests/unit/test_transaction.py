import pytest
from src.transaction import Transaction

@pytest.fixture
def base_transaction_data():
    return {"amount": 100.0, "category": "Food", "date": "2026-01-18"}

class TestTransaction:
    # parametrization: testing multiple categories for correct type assignment
    @pytest.mark.parametrize("category, expected_type", [
        ("Salary", "Income"),
        ("Bonus", "Income"),
        ("Food", "Expense"),
        ("Rent", "Expense"),
        ("Gift", "Income"),
    ])
    def test_transaction_type_assignment(self, category, expected_type):
        transaction = Transaction(amount=100.0, category=category)
        assert transaction.type == expected_type

    # successful creation using a fixture for one case
    def test_transaction_creation_valid_data(self, base_transaction_data):
        transaction = Transaction(**base_transaction_data)
        assert transaction.amount == 100.0
        assert transaction.category == "Food"
        assert transaction.date == "2026-01-18"

    # amount validation (must be positive) - using parametrization for edge cases
    @pytest.mark.parametrize("invalid_amount", [-100.0, 0, "one hundred"])
    def test_transaction_invalid_amounts(self, invalid_amount):
        transaction = Transaction(amount=invalid_amount, category="Rent")
        assert transaction.amount == "Invalid"

    # external ID check (placeholder for mocking later)
    def test_transaction_has_unique_id(self, base_transaction_data):
        transaction = Transaction(**base_transaction_data)
        #to ensure it has some ID attribute
        assert hasattr(transaction, "transaction_id")
        assert len(transaction.transaction_id) > 0