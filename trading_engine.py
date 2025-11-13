import pandas as pd
from typing import Dict, List, Any, Optional
from datetime import datetime
from config import config
from technical_indicators import TechnicalIndicators
from ml_model import lstm_model
from market_simulator import market_sim
from database import db

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
    
    async def analyze_signals(self, symbol: str) -> Dict[str, Any]:
        df = market_sim.get_historical_data(symbol, days=7)
        
        if len(df) < 60:
            return {
                "action": "HOLD",
                "confidence": 0,
                "signals": {},
                "reason": "Insufficient data"
            }
        
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
        
        buy_signals = sum([
            signals['rsi_oversold'],
            signals['ema_bullish'],
            signals['macd_bullish'],
            signals['ml_bullish']
        ])
        
        sell_signals = sum([
            signals['rsi_overbought'],
            signals['ema_bearish'],
            signals['macd_bearish'],
            signals['ml_bearish']
        ])
        
        action = "HOLD"
        confidence = 0
        
        if buy_signals >= 3 and symbol not in self.positions:
            action = "BUY"
            confidence = buy_signals
        elif sell_signals >= 3 and symbol in self.positions:
            action = "SELL"
            confidence = sell_signals
        
        return {
            "action": action,
            "confidence": confidence,
            "signals": signals,
            "indicators": {
                "rsi": round(indicators['rsi'], 2),
                "ema_short": round(indicators['ema_short'], 2),
                "ema_long": round(indicators['ema_long'], 2),
                "macd": round(indicators['macd']['macd'], 2),
                "macd_signal": round(indicators['macd']['signal'], 2),
                "atr": round(indicators['atr'], 2),
                "ml_prediction": round(ml_prediction, 2)
            },
            "current_price": df['close'].iloc[-1]
        }
    
    async def execute_trade(self, symbol: str, action: str, signals: Dict[str, Any]) -> Dict[str, Any]:
        current_data = market_sim.get_current_price(symbol)
        current_price = current_data['price']
        
        if action == "BUY":
            if len(self.positions) >= config.max_positions:
                return {"status": "rejected", "reason": "Max positions reached"}
            
            if symbol in self.positions:
                return {"status": "rejected", "reason": "Position already exists"}
            
            df = market_sim.get_historical_data(symbol, days=7)
            indicators = TechnicalIndicators.calculate_all_indicators(df)
            atr = indicators['atr']
            
            position_value = self.capital * config.position_size_percent
            max_risk = self.capital * config.max_risk_per_trade
            
            stop_loss_distance = atr * config.stop_loss_atr_multiplier
            quantity = int(min(position_value, max_risk / stop_loss_distance) / current_price)
            
            if quantity == 0:
                quantity = 1
            
            cost = quantity * current_price
            
            if cost > self.available_capital:
                return {"status": "rejected", "reason": "Insufficient capital"}
            
            stop_loss = current_price - stop_loss_distance
            take_profit = current_price + (stop_loss_distance * config.take_profit_ratio)
            
            position = Position(symbol, quantity, current_price, stop_loss, take_profit)
            self.positions[symbol] = position
            self.available_capital -= cost
            
            await db.add_trade(symbol, "BUY", quantity, current_price, signals)
            await db.update_position(
                symbol, quantity, current_price, current_price, 0.0, stop_loss, take_profit
            )
            await db.add_log("INFO", f"BUY {quantity} {symbol} @ {current_price}", {
                "stop_loss": stop_loss,
                "take_profit": take_profit
            })
            
            return {
                "status": "executed",
                "action": "BUY",
                "symbol": symbol,
                "quantity": quantity,
                "price": current_price,
                "cost": cost,
                "stop_loss": stop_loss,
                "take_profit": take_profit
            }
        
        elif action == "SELL":
            if symbol not in self.positions:
                return {"status": "rejected", "reason": "No position to sell"}
            
            position = self.positions[symbol]
            position.update_price(current_price)
            
            proceeds = position.quantity * current_price
            self.available_capital += proceeds
            self.total_pnl += position.pnl
            
            await db.add_trade(symbol, "SELL", position.quantity, current_price, signals)
            await db.remove_position(symbol)
            await db.add_log("INFO", f"SELL {position.quantity} {symbol} @ {current_price}", {
                "pnl": position.pnl,
                "entry_price": position.entry_price
            })
            
            result = {
                "status": "executed",
                "action": "SELL",
                "symbol": symbol,
                "quantity": position.quantity,
                "price": current_price,
                "proceeds": proceeds,
                "pnl": position.pnl,
                "entry_price": position.entry_price
            }
            
            del self.positions[symbol]
            return result
        
        return {"status": "rejected", "reason": "Invalid action"}
    
    async def update_positions(self):
        for symbol, position in list(self.positions.items()):
            current_data = market_sim.get_current_price(symbol)
            current_price = current_data['price']
            position.update_price(current_price)
            
            await db.update_position(
                symbol,
                position.quantity,
                position.entry_price,
                current_price,
                position.pnl,
                position.stop_loss,
                position.take_profit
            )
            
            if current_price <= position.stop_loss:
                await self.execute_trade(symbol, "SELL", {"reason": "Stop loss hit"})
                continue
            elif current_price >= position.take_profit:
                await self.execute_trade(symbol, "SELL", {"reason": "Take profit hit"})
                continue
    
    def get_portfolio_summary(self) -> Dict[str, Any]:
        total_position_value = sum(
            pos.current_price * pos.quantity for pos in self.positions.values()
        )
        unrealized_pnl = sum(pos.pnl for pos in self.positions.values())
        
        total_value = self.available_capital + total_position_value
        total_return = ((total_value - config.capital) / config.capital) * 100
        
        return {
            "capital": config.capital,
            "available_capital": round(self.available_capital, 2),
            "invested_capital": round(total_position_value, 2),
            "total_value": round(total_value, 2),
            "unrealized_pnl": round(unrealized_pnl, 2),
            "realized_pnl": round(self.total_pnl, 2),
            "total_pnl": round(unrealized_pnl + self.total_pnl, 2),
            "total_return_percent": round(total_return, 2),
            "open_positions": len(self.positions)
        }

trading_engine = TradingEngine()
