import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List
import random

class MarketSimulator:
    def __init__(self):
        self.symbols = {
            "INFY": {"name": "Infosys", "base_price": 1450.0},
            "RELIANCE": {"name": "Reliance Industries", "base_price": 2450.0},
            "TCS": {"name": "Tata Consultancy Services", "base_price": 3550.0},
            "HDFCBANK": {"name": "HDFC Bank", "base_price": 1650.0},
            "ICICIBANK": {"name": "ICICI Bank", "base_price": 950.0}
        }
        self.historical_data: Dict[str, pd.DataFrame] = {}
        self.current_prices: Dict[str, float] = {}
        self._initialize_historical_data()
    
    def _initialize_historical_data(self):
        for symbol, info in self.symbols.items():
            df = self._generate_historical_data(info["base_price"], days=30)
            self.historical_data[symbol] = df
            self.current_prices[symbol] = df['close'].iloc[-1]
    
    def _generate_historical_data(self, base_price: float, days: int = 30, interval_minutes: int = 1) -> pd.DataFrame:
        periods = days * 375
        
        dates = []
        current_date = datetime.now() - timedelta(days=days)
        
        for day in range(days):
            day_start = current_date.replace(hour=9, minute=15, second=0, microsecond=0)
            for minute in range(375):
                dates.append(day_start + timedelta(minutes=minute))
            current_date += timedelta(days=1)
        
        prices = [base_price]
        volatility = 0.02
        
        for _ in range(periods - 1):
            change = np.random.normal(0, volatility)
            trend = np.random.choice([-0.0005, 0.0005], p=[0.48, 0.52])
            new_price = prices[-1] * (1 + change + trend)
            prices.append(max(new_price, base_price * 0.8))
        
        opens = []
        highs = []
        lows = []
        closes = prices
        volumes = []
        
        for i, close_price in enumerate(closes):
            open_price = prices[i-1] if i > 0 else close_price
            high_price = max(open_price, close_price) * random.uniform(1.0, 1.01)
            low_price = min(open_price, close_price) * random.uniform(0.99, 1.0)
            volume = int(random.uniform(100000, 1000000))
            
            opens.append(open_price)
            highs.append(high_price)
            lows.append(low_price)
            volumes.append(volume)
        
        df = pd.DataFrame({
            'timestamp': dates[:len(prices)],
            'open': opens,
            'high': highs,
            'low': lows,
            'close': closes,
            'volume': volumes
        })
        
        return df
    
    def get_historical_data(self, symbol: str, days: int = 7) -> pd.DataFrame:
        if symbol not in self.historical_data:
            return pd.DataFrame()
        
        df = self.historical_data[symbol].copy()
        cutoff_date = datetime.now() - timedelta(days=days)
        df = df[df['timestamp'] >= cutoff_date]
        return df
    
    def get_current_price(self, symbol: str) -> Dict[str, float]:
        if symbol not in self.current_prices:
            return {"price": 0.0, "change": 0.0, "change_percent": 0.0}
        
        current = self.current_prices[symbol]
        df = self.historical_data[symbol]
        previous = df['close'].iloc[-2] if len(df) > 1 else current
        
        change = current - previous
        change_percent = (change / previous) * 100
        
        return {
            "symbol": symbol,
            "name": self.symbols[symbol]["name"],
            "price": round(current, 2),
            "change": round(change, 2),
            "change_percent": round(change_percent, 2),
            "open": round(df['open'].iloc[-1], 2),
            "high": round(df['high'].iloc[-1], 2),
            "low": round(df['low'].iloc[-1], 2),
            "volume": int(df['volume'].iloc[-1])
        }
    
    def update_prices(self):
        for symbol in self.symbols.keys():
            df = self.historical_data[symbol]
            last_price = df['close'].iloc[-1]
            
            volatility = 0.02
            change = np.random.normal(0, volatility)
            trend = np.random.choice([-0.0005, 0.0005], p=[0.48, 0.52])
            new_price = last_price * (1 + change + trend)
            new_price = max(new_price, self.symbols[symbol]["base_price"] * 0.8)
            
            new_row = {
                'timestamp': datetime.now(),
                'open': last_price,
                'high': max(last_price, new_price) * random.uniform(1.0, 1.005),
                'low': min(last_price, new_price) * random.uniform(0.995, 1.0),
                'close': new_price,
                'volume': int(random.uniform(100000, 1000000))
            }
            
            self.historical_data[symbol] = pd.concat([
                df,
                pd.DataFrame([new_row])
            ], ignore_index=True).tail(10000)
            
            self.current_prices[symbol] = new_price
    
    def get_all_symbols(self) -> List[Dict[str, str]]:
        return [
            {"symbol": symbol, "name": info["name"]}
            for symbol, info in self.symbols.items()
        ]

market_sim = MarketSimulator()
