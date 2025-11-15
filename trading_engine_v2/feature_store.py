import pandas as pd
from typing import List, Dict, Any

class FeatureStore:
    """
    Calculates and stores technical indicators and other features for trading.
    Designed to update incrementally as new data streams in.
    """

    def __init__(self, symbols: List[str]):
        self.features: Dict[str, pd.DataFrame] = {symbol: pd.DataFrame() for symbol in symbols}

    def add_candle(self, candle: Dict[str, Any]):
        """
        Adds a new candle and updates the features for the corresponding symbol.
        """
        symbol = candle["symbol"]
        if symbol not in self.features:
            self.features[symbol] = pd.DataFrame()

        new_candle_df = pd.DataFrame([candle])
        self.features[symbol] = pd.concat([self.features[symbol], new_candle_df], ignore_index=True)
        self._calculate_features(symbol)

    def _calculate_features(self, symbol: str):
        """
        Calculates all the features for a given symbol.
        """
        df = self.features[symbol]
        if df.empty:
            return

        # Simple Moving Average (SMA)
        df["sma_20"] = df["close"].rolling(window=20).mean()

        # Exponential Moving Average (EMA)
        df["ema_20"] = df["close"].ewm(span=20, adjust=False).mean()

        # Relative Strength Index (RSI)
        delta = df["close"].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        df["rsi"] = 100 - (100 / (1 + rs))

        # Average True Range (ATR)
        high_low = df["high"] - df["low"]
        high_close = (df["high"] - df["close"].shift()).abs()
        low_close = (df["low"] - df["close"].shift()).abs()
        tr = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
        df["atr"] = tr.rolling(window=14).mean()

        # Volume Weighted Average Price (VWAP)
        df["vwap"] = (df["volume"] * (df["high"] + df["low"]) / 2).cumsum() / df["volume"].cumsum()

        self.features[symbol] = df

    def get_features(self, symbol: str) -> pd.DataFrame:
        """
        Returns the DataFrame with all the features for a given symbol.
        """
        return self.features.get(symbol, pd.DataFrame())

    def get_latest_features(self, symbol: str) -> Dict[str, Any]:
        """
        Returns the latest features for a given symbol.
        """
        df = self.get_features(symbol)
        if not df.empty:
            return df.iloc[-1].to_dict()
        return {}
