import pytest
import pandas as pd
from trading_engine_v2.feature_store import FeatureStore

@pytest.fixture
def feature_store():
    return FeatureStore(symbols=["NSE:INFY"])

def test_add_candle(feature_store):
    candle = {"symbol": "NSE:INFY", "close": 1500.0, "high": 1510.0, "low": 1490.0, "volume": 1000}
    feature_store.add_candle(candle)
    features = feature_store.get_features("NSE:INFY")
    assert not features.empty
    assert features.iloc[-1]["close"] == 1500.0

def test_calculate_features(feature_store):
    # Add enough data to calculate features
    for i in range(20):
        candle = {"symbol": "NSE:INFY", "close": 1500.0 + i, "high": 1510.0 + i, "low": 1490.0 + i, "volume": 1000}
        feature_store.add_candle(candle)

    features = feature_store.get_features("NSE:INFY")
    assert "sma_20" in features.columns
    assert "ema_20" in features.columns
    assert "rsi" in features.columns
    assert "atr" in features.columns
    assert "vwap" in features.columns
