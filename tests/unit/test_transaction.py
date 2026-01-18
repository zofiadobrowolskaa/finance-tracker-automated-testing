import pytest
from src.transaction import Transaction

class TestTransaction:
    # successful creation of an expense
    def test_transaction_expense_creation(self):
        transaction = Transaction(amount=50.0, category="Food", date="2026-01-18")
        assert transaction.amount == 50.0
        assert transaction.category == "Food"
        assert transaction.type == "Expense"
        assert transaction.date == "2026-01-18"

    # successful creation of an income
    def test_transaction_income_creation(self):
        transaction = Transaction(amount=5000.0, category="Salary", date="2026-01-01")
        assert transaction.amount == 5000.0
        assert transaction.type == "Income"

    # amount validation (must be positive)
    def test_transaction_invalid_amount_negative(self):
        transaction = Transaction(amount=-100.0, category="Rent", date="2026-01-15")
        assert transaction.amount == "Invalid"

    def test_transaction_invalid_amount_zero(self):
        transaction = Transaction(amount=0.0, category="Gift", date="2026-01-15")
        assert transaction.amount == "Invalid"

    # external ID (placeholder for mocking later)
    def test_transaction_has_unique_id(self):
        transaction = Transaction(amount=100.0, category="Utilities", date="2026-01-15")
        # to ensure it has some ID attribute
        assert hasattr(transaction, "transaction_id")