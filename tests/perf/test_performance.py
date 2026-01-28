import pytest
import requests

class TestPerformance:
    
    url = "http://127.0.0.1:5000"
    timeout = 1.0

    transaction_data = {
        "amount": 100.0,
        "category": "TestPerf",
        "date": "2026-01-24"
    }
    iteration_count = 100
    
    # clean up before and after tests
    @pytest.fixture(autouse=True)
    def setup_and_teardown(self):
        self._clear_registry()
        yield
        self._clear_registry()

    def _clear_registry(self):
        try:
            response = requests.get(f"{self.url}/api/transactions", timeout=self.timeout)
            if response.status_code == 200:
                for t in response.json():
                    requests.delete(f"{self.url}/api/transactions/{t['transaction_id']}", timeout=self.timeout)
        except Exception:
            pass

    # rapid creation of transactions
    def test_create_transaction_performance(self):
        for _ in range(self.iteration_count):
            response = requests.post(f"{self.url}/api/transactions", json=self.transaction_data, timeout=self.timeout)
            assert response.status_code == 201

    # rapid reading of summary (calculation load)
    def test_get_summary_performance(self):
    
        for _ in range(10):
            requests.post(f"{self.url}/api/transactions", json=self.transaction_data, timeout=self.timeout)
        
        for _ in range(self.iteration_count):
            response = requests.get(f"{self.url}/api/summary", timeout=self.timeout)
            assert response.status_code == 200
            assert "balance" in response.json()

    # create and delete cycle
    def test_create_and_delete_cycle(self):
        for _ in range(50): # smaller loop as it involves more operations
            requests.post(f"{self.url}/api/transactions", json=self.transaction_data, timeout=self.timeout)
            
            history_response = requests.get(f"{self.url}/api/transactions", timeout=self.timeout)
            history = history_response.json()
            t_id = history[-1]["transaction_id"]
            
            delete_resp = requests.delete(f"{self.url}/api/transactions/{t_id}", timeout=self.timeout)
            assert delete_resp.status_code == 200