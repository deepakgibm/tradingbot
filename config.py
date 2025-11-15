from pydantic_settings import BaseSettings
from typing import List

class TradingConfig(BaseSettings):
    capital: float = 200000.0
    max_risk_per_trade: float = 0.01
    max_positions: int = 5
    position_size_percent: float = 0.20
    
    rsi_oversold: int = 30
    rsi_overbought: int = 70
    ema_short: int = 20
    ema_long: int = 50
    
    sequence_length: int = 60
    lstm_units: List[int] = [100, 50]
    dropout_rate: float = 0.3
    
    stop_loss_atr_multiplier: float = 2.0
    take_profit_ratio: float = 2.0
    
    simulation_mode: bool = True
    auto_square_off_time: str = "15:15"

    class Config:
        env_file = ".env"

config = TradingConfig()
