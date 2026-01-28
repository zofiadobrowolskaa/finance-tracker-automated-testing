import pytest
import requests

class TestFinanceAPI:

    url = "http://127.0.0.1:5000"

    transaction_data = {
        "amount": 150.0,
        "category": "Groceries",
        "date": "2026-01-18"
    }

    # cleanup before each test to ensure isolation
    @pytest.fixture(autouse=True)
    def setup_and_teardown(self):
        try:
            # get all transactions and delete them
            response = requests.get(f"{self.url}/api/transactions")
            if response.status_code == 200:
                for t in response.json():
                    requests.delete(f"{self.url}/api/transactions/{t['transaction_id']}")
        except Exception:
            pytest.fail("API server is not running. Start Flask before running tests.")
        yield

    # creating a new transaction via POST
    def test_create_transaction(self):
        response = requests.post(f"{self.url}/api/transactions", json=self.transaction_data)
        assert response.status_code == 201
        assert response.json()["message"] == "Transaction added"

    # getting full transaction history via GET
    def test_get_history(self):
        requests.post(f"{self.url}/api/transactions", json=self.transaction_data)
        
        response = requests.get(f"{self.url}/api/transactions")
        assert response.status_code == 200
        assert len(response.json()) >= 1
        assert response.json()[0]["category"] == "Groceries"

    # getting account summary (balance and status)
    def test_get_summary(self):
        response = requests.get(f"{self.url}/api/summary")
        assert response.status_code == 200
        data = response.json()
        assert "balance" in data
        assert "budget_status" in data

    # deleting a transaction via DELETE
    def test_delete_transaction(self):
        requests.post(f"{self.url}/api/transactions", json=self.transaction_data)
        
        t_id = requests.get(f"{self.url}/api/transactions").json()[0]["transaction_id"]
        
        response = requests.delete(f"{self.url}/api/transactions/{t_id}")
        assert response.status_code == 200
        assert response.json()["message"] == "Transaction deleted"
        
        history = requests.get(f"{self.url}/api/transactions").json()
        assert len(history) == 0
    
    # updating transaction category via PATCH
    def test_update_transaction(self):
        requests.post(f"{self.url}/api/transactions", json=self.transaction_data)
        t_id = requests.get(f"{self.url}/api/transactions").json()[0]["transaction_id"]
        
        # changing from expense to income
        update_body = {"category": "Salary"}
        response = requests.patch(f"{self.url}/api/transactions/{t_id}", json=update_body)
        
        assert response.status_code == 200
        assert response.json()["message"] == "Transaction updated"
        
        # verify update
        updated_t = requests.get(f"{self.url}/api/transactions").json()[0]
        assert updated_t["category"] == "Salary"
        assert updated_t["type"] == "Income"

    # test missing data
    def test_create_transaction_invalid_body(self):
        response = requests.post(f"{self.url}/api/transactions", json={"category": "Food"})
        assert response.status_code == 400
        assert response.json()["message"] == "Invalid body"

    # test business logic error, e.g., negative amount
    def test_create_transaction_logic_error(self):
        invalid_data = {"amount": -100, "category": "Test"}
        response = requests.post(f"{self.url}/api/transactions", json=invalid_data)
        assert response.status_code == 422
        assert response.json()["message"] == "Invalid transaction data"

    # test deleting non-existent ID
    def test_delete_non_existent(self):
        response = requests.delete(f"{self.url}/api/transactions/fake_id_123")
        assert response.status_code == 404
        assert response.json()["message"] == "Transaction not found"

    # test updating non-existent ID
    def test_update_non_existent(self):
        response = requests.patch(f"{self.url}/api/transactions/fake_id_123", json={"category": "Food"})
        assert response.status_code == 404
        assert response.json()["message"] == "Transaction not found"