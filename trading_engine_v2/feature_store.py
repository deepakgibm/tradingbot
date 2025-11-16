import pandas as pd
from typing import List, Dict, Any

class FeatureStore:
    """
    Calculates and stores technical indicators and other features for trading.
    Designed to update incrementally as new data streams in.
    """

    def __init__(self, symbols: List[str], timeframes: List[str] = ['1min']):
        self.features: Dict[str, Dict[str, pd.DataFrame]] = {
            symbol: {tf: pd.DataFrame() for tf in timeframes} for symbol in symbols
        }
        self.timeframes = timeframes

    def add_candle(self, candle: Dict[str, Any]):
        """
        Adds a new candle and updates the features for the corresponding symbol.
        """
        symbol = candle["symbol"]
        if symbol not in self.features:
            self.features[symbol] = {tf: pd.DataFrame() for tf in self.timeframes}

        new_candle_df = pd.DataFrame([candle])
        new_candle_df['timestamp'] = pd.to_datetime(new_candle_df['ts'], unit='s')
        new_candle_df.set_index('timestamp', inplace=True)

        base_tf = self.timeframes[0]
        self.features[symbol][base_tf] = pd.concat([self.features[symbol][base_tf], new_candle_df])

        for tf in self.timeframes:
            self._resample_and_calculate(symbol, base_tf, tf)

    def _resample_and_calculate(self, symbol: str, base_tf: str, target_tf: str):
        """
        Resamples the base timeframe data to the target timeframe and calculates features.
        """
        base_df = self.features[symbol][base_tf]
        resampled_df = base_df.resample(target_tf).agg({
            'open': 'first',
            'high': 'max',
            'low': 'min',
            'close': 'last',
            'volume': 'sum'
        }).dropna()

        self.features[symbol][target_tf] = resampled_df
        self._calculate_features(symbol, target_tf)

    def _calculate_features(self, symbol: str, timeframe: str):
        """
        Calculates all the features for a given symbol and timeframe.
        """
        df = self.features[symbol][timeframe]
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

        self.features[symbol][timeframe] = df

    def get_features(self, symbol: str, timeframe: str) -> pd.DataFrame:
        """
        Returns the DataFrame with all the features for a given symbol and timeframe.
        """
        return self.features.get(symbol, {}).get(timeframe, pd.DataFrame())

    def get_latest_features(self, symbol: str, timeframe: str) -> Dict[str, Any]:
        """
        Returns the latest features for a given symbol and timeframe.
        """
        df = self.get_features(symbol, timeframe)
        if not df.empty:
            return df.iloc[-1].to_dict()
        return {}
