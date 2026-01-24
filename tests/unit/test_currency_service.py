import pytest
from unittest.mock import patch
from src.utils.currency_service import CurrencyService

class TestCurrencyService:
    
    # successful exchange rate retrieval
    @patch('requests.get')
    def test_get_exchange_rate_usd(self, mock_get):
        # prepare the mock - fake NBP response
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            "rates": [
                {"mid": 4.0}  # we force the rate to be 4.0
            ]
        }

        service = CurrencyService()
        rate = service.get_exchange_rate("USD")

        assert rate == 4.0
        
        mock_get.assert_called_once_with("http://api.nbp.pl/api/exchangerates/rates/a/USD/?format=json")

    # API connection error
    @patch('requests.get')
    def test_get_exchange_rate_connection_error(self, mock_get):
        mock_get.return_value.status_code = 404
        
        service = CurrencyService()
        rate = service.get_exchange_rate("EUR")

        assert rate is None

    # invalid JSON format
    @patch('requests.get')
    def test_get_exchange_rate_invalid_json(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {}

        service = CurrencyService()
        rate = service.get_exchange_rate("GBP")
        
        assert rate is None