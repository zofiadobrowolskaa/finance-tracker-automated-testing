import requests

class CurrencyService:
    def get_exchange_rate(self, currency_code):
        url = f"http://api.nbp.pl/api/exchangerates/rates/a/{currency_code}/?format=json"
        
        try:
            response = requests.get(url)
            
            if response.status_code == 200:
                data = response.json()
                # NBP returns structure: {"rates": [{"mid": 4.1234, ...}]}
                return data.get("rates", [{}])[0].get("mid")
            
            return None
            
        except (requests.RequestException, ValueError, IndexError):
            return None