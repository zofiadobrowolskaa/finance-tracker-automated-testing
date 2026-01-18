import pytest
import requests

class TestFinanceAPI:
    url = "http://127.0.0.1:5000/api"
    
    transaction_data = {
        "amount": 150.0,
        "category": "Groceries",
        "date": "2026-01-18"
    }

    # cleanup before each test to ensure isolation
    @pytest.fixture(autouse=True)
    def setup_and_teardown(self):
        # get all transactions and delete them
        response = requests.get(f"{self.url}/transactions")
        if response.status_code == 200:
            for t in response.json():
                requests.delete(f"{self.url}/transactions/{t['transaction_id']}")
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

    # deleting a transaction via DELETE
    def test_delete_transaction(self):
        requests.post(f"{self.url}/transactions", json=self.transaction_data)
        t_id = requests.get(f"{self.url}/transactions").json()[0]["transaction_id"]
        
        response = requests.delete(f"{self.url}/transactions/{t_id}")
        assert response.status_code == 200
        assert response.json()["message"] == "Transaction deleted"
        
        history = requests.get(f"{self.url}/transactions").json()
        assert len(history) == 0
    
    # updating transaction category via PATCH
    def test_update_transaction(self):
        # create and get the ID
        requests.post(f"{self.url}/transactions", json=self.transaction_data)
        t_id = requests.get(f"{self.url}/transactions").json()[0]["transaction_id"]
        
        # changing from expense to income
        update_body = {"category": "Salary"}
        response = requests.patch(f"{self.url}/transactions/{t_id}", json=update_body)
        
        assert response.status_code == 200
        assert response.json()["message"] == "Transaction updated"
        
        # verify update
        updated_t = requests.get(f"{self.url}/transactions").json()[0]
        assert updated_t["category"] == "Salary"
        assert updated_t["type"] == "Income"