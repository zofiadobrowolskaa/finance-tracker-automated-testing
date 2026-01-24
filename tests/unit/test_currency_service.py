import pytest
import requests # <--- WAŻNE: Dodaj ten import
from unittest.mock import patch
from src.utils.currency_service import CurrencyService

class TestCurrencyService:
    
    # parametrization: verify that logic works for different currencies and rates
    @pytest.mark.parametrize("currency, mock_rate", [
        ("USD", 4.0),
        ("EUR", 4.5),
        ("GBP", 5.2)
    ])
    # successful exchange rate retrieval
    @patch('requests.get')
    def test_get_exchange_rate_success(self, mock_get, currency, mock_rate):
        # prepare the mock - fake NBP response
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            "rates": [
                {"mid": mock_rate}
            ]
        }

        service = CurrencyService()
        rate = service.get_exchange_rate(currency)

        assert rate == mock_rate

        # verify correct URL construction for each currency
        expected_url = f"http://api.nbp.pl/api/exchangerates/rates/a/{currency}/?format=json"
        mock_get.assert_called_once_with(expected_url)

    # API connection error (HTTP 404)
    @patch('requests.get')
    def test_get_exchange_rate_not_found(self, mock_get):
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
    
    # network exception (simulating e.g. no internet connection)
    @patch('requests.get')
    def test_get_exchange_rate_network_exception(self, mock_get):
        # side effect forces the mock to raise an exception instead of returning a value
        mock_get.side_effect = requests.RequestException("Connection error")
        
        service = CurrencyService()
        rate = service.get_exchange_rate("USD")
        
        # should return None because exception is caught in the try-except block
        assert rate is None