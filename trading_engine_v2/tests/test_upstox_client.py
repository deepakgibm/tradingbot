import pytest
from unittest.mock import patch, Mock
from trading_engine_v2.upstox_client import UpstoxClient

@pytest.fixture
def client():
    return UpstoxClient()

@patch("requests.Session.request")
def test_get_instrument_master(mock_request, client):
    mock_response = Mock()
    mock_response.json.return_value = [{"instrument_key": "NSE_EQ|INE848E01016"}]
    mock_request.return_value = mock_response

    result = client.get_instrument_master()
    assert result is not None
    assert result[0]["instrument_key"] == "NSE_EQ|INE848E01016"

@patch("requests.Session.request")
def test_fetch_historical(mock_request, client):
    mock_response = Mock()
    mock_response.json.return_value = {"candles": []}
    mock_request.return_value = mock_response

    result = client.fetch_historical("NSE_EQ|INE848E01016", "2023-01-01", "2023-01-02", "1minute")
    assert result is not None
    assert "candles" in result

def test_place_order(client):
    order_spec = {"symbol": "NSE:INFY", "side": "BUY", "size": 100}
    result = client.place_order(order_spec)
    assert result["status"] == "success"
    assert "order_id" in result

def test_get_order_status(client):
    result = client.get_order_status("mock_order_123")
    assert result["status"] == "completed"
