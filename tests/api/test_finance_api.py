import pytest
from src.app.api import app

class TestFinanceAPI:
    
    transaction_data = {
        "amount": 150.0,
        "category": "Groceries",
        "date": "2026-01-18"
    }

    # fixture providing the Flask test client
    @pytest.fixture
    def client(self):
        app.config['TESTING'] = True
        with app.test_client() as client:
            yield client

    # cleanup before each test to ensure isolation
    @pytest.fixture(autouse=True)
    def setup_and_teardown(self, client):
        # get all transactions and delete them
        response = client.get("/api/transactions")
        if response.status_code == 200:
            for t in response.json:
                client.delete(f"/api/transactions/{t['transaction_id']}")
        yield

    # creating a new transaction via POST
    def test_create_transaction(self, client):
        response = client.post("/api/transactions", json=self.transaction_data)
        assert response.status_code == 201
        assert response.json["message"] == "Transaction added"

    # getting full transaction history via GET
    def test_get_history(self, client):
        client.post("/api/transactions", json=self.transaction_data)
        
        response = client.get("/api/transactions")
        assert response.status_code == 200
        assert len(response.json) >= 1
        assert response.json[0]["category"] == "Groceries"

    # getting account summary (balance and status)
    def test_get_summary(self, client):
        response = client.get("/api/summary")
        assert response.status_code == 200
        data = response.json
        assert "balance" in data
        assert "budget_status" in data

    # deleting a transaction via DELETE
    def test_delete_transaction(self, client):
        client.post("/api/transactions", json=self.transaction_data)
        
        t_id = client.get("/api/transactions").json[0]["transaction_id"]
        
        response = client.delete(f"/api/transactions/{t_id}")
        assert response.status_code == 200
        assert response.json["message"] == "Transaction deleted"
        
        history = client.get("/api/transactions").json
        assert len(history) == 0
    
    # updating transaction category via PATCH
    def test_update_transaction(self, client):
        client.post("/api/transactions", json=self.transaction_data)
        t_id = client.get("/api/transactions").json[0]["transaction_id"]
        
        # changing from expense to income
        update_body = {"category": "Salary"}
        response = client.patch(f"/api/transactions/{t_id}", json=update_body)
        
        assert response.status_code == 200
        assert response.json["message"] == "Transaction updated"
        
        # verify update
        updated_t = client.get("/api/transactions").json[0]
        assert updated_t["category"] == "Salary"
        assert updated_t["type"] == "Income"

    # test missing data
    def test_create_transaction_invalid_body(self, client):
        response = client.post("/api/transactions", json={"category": "Food"})
        assert response.status_code == 400
        assert response.json["message"] == "Invalid body"

    # test business logic error, e.g., negative amount
    def test_create_transaction_logic_error(self, client):
        invalid_data = {"amount": -100, "category": "Test"}
        response = client.post("/api/transactions", json=invalid_data)
        assert response.status_code == 422
        assert response.json["message"] == "Invalid transaction data"

    # test deleting non-existent ID
    def test_delete_non_existent(self, client):
        response = client.delete("/api/transactions/fake_id_123")
        assert response.status_code == 404
        assert response.json["message"] == "Transaction not found"

    # test updating non-existent ID
    def test_update_non_existent(self, client):
        response = client.patch("/api/transactions/fake_id_123", json={"category": "Food"})
        assert response.status_code == 404
        assert response.json["message"] == "Transaction not found"