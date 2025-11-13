import pandas as pd
import numpy as np
from typing import Dict, Any

class TechnicalIndicators:
    @staticmethod
    def calculate_rsi(data: pd.Series, period: int = 14) -> float:
        delta = data.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi.iloc[-1] if len(rsi) > 0 else 50.0
    
    @staticmethod
    def calculate_ema(data: pd.Series, period: int) -> float:
        ema = data.ewm(span=period, adjust=False).mean()
        return ema.iloc[-1] if len(ema) > 0 else data.iloc[-1]
    
    @staticmethod
    def calculate_macd(data: pd.Series, fast: int = 12, slow: int = 26, signal: int = 9) -> Dict[str, float]:
        ema_fast = data.ewm(span=fast, adjust=False).mean()
        ema_slow = data.ewm(span=slow, adjust=False).mean()
        macd_line = ema_fast - ema_slow
        signal_line = macd_line.ewm(span=signal, adjust=False).mean()
        
        return {
            "macd": macd_line.iloc[-1] if len(macd_line) > 0 else 0.0,
            "signal": signal_line.iloc[-1] if len(signal_line) > 0 else 0.0,
            "histogram": (macd_line.iloc[-1] - signal_line.iloc[-1]) if len(macd_line) > 0 else 0.0
        }
    
    @staticmethod
    def calculate_atr(high: pd.Series, low: pd.Series, close: pd.Series, period: int = 14) -> float:
        high_low = high - low
        high_close = np.abs(high - close.shift())
        low_close = np.abs(low - close.shift())
        
        ranges = pd.concat([high_low, high_close, low_close], axis=1)
        true_range = ranges.max(axis=1)
        atr = true_range.rolling(window=period).mean()
        
        return atr.iloc[-1] if len(atr) > 0 else 1.0
    
    @staticmethod
    def calculate_all_indicators(df: pd.DataFrame) -> Dict[str, Any]:
        if len(df) < 50:
            return {
                "rsi": 50.0,
                "ema_short": df['close'].iloc[-1],
                "ema_long": df['close'].iloc[-1],
                "macd": {"macd": 0.0, "signal": 0.0, "histogram": 0.0},
                "atr": 1.0
            }
        
        return {
            "rsi": TechnicalIndicators.calculate_rsi(df['close']),
            "ema_short": TechnicalIndicators.calculate_ema(df['close'], 20),
            "ema_long": TechnicalIndicators.calculate_ema(df['close'], 50),
            "macd": TechnicalIndicators.calculate_macd(df['close']),
            "atr": TechnicalIndicators.calculate_atr(df['high'], df['low'], df['close'])
        }
