import pytest
from trading_engine_v2.risk_manager import RiskManager

@pytest.fixture
def risk_manager():
    return RiskManager(capital=100000.0)

def test_size_position(risk_manager):
    size = risk_manager.size_position(entry_price=100, stop_loss_price=90, symbol="NSE:INFY")
    assert size == 100

def test_check_exposure(risk_manager):
    assert risk_manager.check_exposure(new_position_value=10000, current_exposure=0)
    assert not risk_manager.check_exposure(new_position_value=30000, current_exposure=0)

def test_manage_signal(risk_manager):
    signal = {"symbol": "NSE:INFY", "side": "BUY", "price": 100, "stop": 90}
    result = risk_manager.manage_signal(signal)
    assert result["action"] == "place_order"
    assert "order_spec" in result
    assert result["order_spec"]["size"] == 100
