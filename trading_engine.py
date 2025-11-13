import pandas as pd
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime, date
from config import config
from technical_indicators import TechnicalIndicators
from ml_model import lstm_model
from upstox_client import upstox_client_instance
from database import db

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Position:
    def __init__(self, symbol: str, quantity: int, entry_price: float, stop_loss: float, take_profit: float):
        self.symbol = symbol
        self.quantity = quantity
        self.entry_price = entry_price
        self.stop_loss = stop_loss
        self.take_profit = take_profit
        self.current_price = entry_price
        self.pnl = 0.0
        self.entry_time = datetime.now()

    def update_price(self, current_price: float):
        self.current_price = current_price
        self.pnl = (current_price - self.entry_price) * self.quantity

    def to_dict(self) -> Dict[str, Any]:
        return {
            "symbol": self.symbol,
            "quantity": self.quantity,
            "entry_price": round(self.entry_price, 2),
            "current_price": round(self.current_price, 2),
            "stop_loss": round(self.stop_loss, 2),
            "take_profit": round(self.take_profit, 2),
            "pnl": round(self.pnl, 2),
            "pnl_percent": round((self.pnl / (self.entry_price * self.quantity)) * 100, 2),
            "entry_time": self.entry_time.isoformat()
        }

class TradingEngine:
    def __init__(self):
        self.positions: Dict[str, Position] = {}
        self.capital = config.capital
        self.available_capital = config.capital
        self.total_pnl = 0.0
        self.is_running = False

    async def analyze_signals(self, symbol: str, instrument_key: str) -> Dict[str, Any]:
        logging.info(f"Analyzing signals for {symbol} ({instrument_key})")
        today = date.today()
        from_date = today.replace(day=today.day - 7).strftime('%Y-%m-%d')
        to_date = today.strftime('%Y-%m-%d')

        historical_data = upstox_client_instance.get_historical_candle_data(
            instrument_key, '1minute', to_date, from_date
        )

        if historical_data['status'] != 'success' or not historical_data['data'].payload.candles:
            logging.warning(f"Insufficient data for {symbol}")
            return {"action": "HOLD", "reason": "Insufficient data"}

        candles = historical_data['data'].payload.candles
        df = pd.DataFrame(candles, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume', 'oi'])
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df.set_index('timestamp', inplace=True)

        if len(df) < 60:
            logging.warning(f"Insufficient data for {symbol} (less than 60 candles)")
            return {"action": "HOLD", "reason": "Insufficient data"}
        
        indicators = TechnicalIndicators.calculate_all_indicators(df)
        ml_prediction = lstm_model.predict(df)
        
        signals = {
            "rsi_oversold": indicators['rsi'] < config.rsi_oversold,
            "rsi_overbought": indicators['rsi'] > config.rsi_overbought,
            "ema_bullish": indicators['ema_short'] > indicators['ema_long'],
            "ema_bearish": indicators['ema_short'] < indicators['ema_long'],
            "macd_bullish": indicators['macd']['macd'] > indicators['macd']['signal'],
            "macd_bearish": indicators['macd']['macd'] < indicators['macd']['signal'],
            "ml_bullish": ml_prediction > 0.5,
            "ml_bearish": ml_prediction < -0.5
        }
        
        buy_signals = sum([signals['rsi_oversold'], signals['ema_bullish'], signals['macd_bullish'], signals['ml_bullish']])
        sell_signals = sum([signals['rsi_overbought'], signals['ema_bearish'], signals['macd_bearish'], signals['ml_bearish']])
        
        action = "HOLD"
        if buy_signals >= 3 and symbol not in self.positions:
            action = "BUY"
        elif sell_signals >= 3 and symbol in self.positions:
            action = "SELL"
        
        logging.info(f"Signal for {symbol}: {action} (Buy: {buy_signals}, Sell: {sell_signals})")
        return {"action": action, "signals": signals}
    
    async def execute_trade(self, symbol: str, instrument_key: str, action: str, signals: Dict[str, Any]) -> Dict[str, Any]:
        logging.info(f"Executing {action} trade for {symbol} ({instrument_key})")
        # Fetch current price from Upstox - Placeholder
        current_price = 100.0

        if action == "BUY":
            position_value = self.capital * config.position_size_percent
            max_risk = self.capital * config.max_risk_per_trade
            stop_loss_distance = 2 * config.stop_loss_atr_multiplier # Placeholder ATR
            quantity = int(min(position_value, max_risk / stop_loss_distance) / current_price)
            if quantity == 0:
                quantity = 1

            order_details = {
                "quantity": quantity, "product": "D", "validity": "DAY", "price": 0,
                "instrument_token": instrument_key, "order_type": "MARKET", "transaction_type": "BUY",
                "disclosed_quantity": 0, "trigger_price": 0, "is_amo": False
            }
            order_response = upstox_client_instance.place_order(order_details)

            if order_response['status'] == 'success':
                logging.info(f"Successfully placed BUY order for {symbol}")
                return {"status": "executed", "details": order_response['data']}
            else:
                logging.error(f"Failed to place BUY order for {symbol}: {order_response['message']}")
                return {"status": "rejected", "reason": order_response['message']}

        elif action == "SELL":
            if symbol in self.positions:
                position = self.positions[symbol]
                order_details = {
                    "quantity": position.quantity, "product": "D", "validity": "DAY", "price": 0,
                    "instrument_token": instrument_key, "order_type": "MARKET", "transaction_type": "SELL",
                    "disclosed_quantity": 0, "trigger_price": 0, "is_amo": False
                }
                order_response = upstox_client_instance.place_order(order_details)

                if order_response['status'] == 'success':
                    logging.info(f"Successfully placed SELL order for {symbol}")
                    del self.positions[symbol]
                    return {"status": "executed", "details": order_response['data']}
                else:
                    logging.error(f"Failed to place SELL order for {symbol}: {order_response['message']}")
                    return {"status": "rejected", "reason": order_response['message']}
            else:
                logging.warning(f"Attempted to sell {symbol} without a position.")
                return {"status": "rejected", "reason": "No position to sell"}

        return {"status": "rejected", "reason": "Invalid action"}
    
    async def update_positions(self):
        pass
    
    def get_portfolio_summary(self) -> Dict[str, Any]:
        return {}

trading_engine = TradingEngine()
