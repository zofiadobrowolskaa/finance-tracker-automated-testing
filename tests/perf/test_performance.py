import pytest
from src.app.api import app

class TestPerformance:
    
    transaction_data = {
        "amount": 100.0,
        "category": "TestPerf",
        "date": "2026-01-24"
    }
    iteration_count = 100
    
    # fixture providing the Flask test client
    @pytest.fixture
    def client(self):
        app.config['TESTING'] = True
        with app.test_client() as client:
            yield client

    # clean up before and after tests
    @pytest.fixture(autouse=True)
    def setup_and_teardown(self, client):
        self._clear_registry(client)
        yield
        self._clear_registry(client)

    def _clear_registry(self, client):
        try:
            response = client.get("/api/transactions")
            if response.status_code == 200:
                for t in response.json:
                    client.delete(f"/api/transactions/{t['transaction_id']}")
        except Exception:
            pass

    # rapid creation of transactions
    def test_create_transaction_performance(self, client):
        for _ in range(self.iteration_count):
            response = client.post("/api/transactions", json=self.transaction_data)
            assert response.status_code == 201

    # rapid reading of summary (calculation load)
    def test_get_summary_performance(self, client):
        for _ in range(10):
            client.post("/api/transactions", json=self.transaction_data)
        
        for _ in range(self.iteration_count):
            response = client.get("/api/summary")
            assert response.status_code == 200
            assert "balance" in response.json

    # create and delete cycle
    def test_create_and_delete_cycle(self, client):
        for _ in range(50): # smaller loop as it involves more operations
            client.post("/api/transactions", json=self.transaction_data)
            
            history = client.get("/api/transactions").json
            t_id = history[-1]["transaction_id"]
            
            delete_resp = client.delete(f"/api/transactions/{t_id}")
            assert delete_resp.status_code == 200