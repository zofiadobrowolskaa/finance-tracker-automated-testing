import pytest
import requests

class TestFinanceAPI:
    url = "http://127.0.0.1:5000/api"
    
    transaction_data = {
        "amount": 150.0,
        "category": "Groceries",
        "date": "2026-01-18"
    }

    @pytest.fixture(autouse=True)
    def setup_and_teardown(self):
        yield

    # creating a new transaction via POST
    def test_create_transaction(self):
        response = requests.post(f"{self.url}/transactions", json=self.transaction_data)
        assert response.status_code == 201
        assert response.json()["message"] == "Transaction added"

    # getting full transaction history via GET
    def test_get_history(self):
        # first, ensure there is at least one transaction
        requests.post(f"{self.url}/transactions", json=self.transaction_data)
        
        response = requests.get(f"{self.url}/transactions")
        assert response.status_code == 200
        assert len(response.json()) >= 1
        assert response.json()[0]["category"] == "Groceries"

    # getting account summary (balance and status)
    def test_get_summary(self):
        response = requests.get(f"{self.url}/summary")
        assert response.status_code == 200
        data = response.json()
        assert "balance" in data
        assert "budget_status" in data