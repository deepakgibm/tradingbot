from pydantic import BaseModel
from typing import List, Optional

class Tick(BaseModel):
    symbol: str
    ts: int
    bid: float
    ask: float
    last: float
    volume: int

class Candle(BaseModel):
    symbol: str
    interval: str
    open: float
    high: float
    low: float
    close: float
    volume: int
    ts: int

class TradingSignal(BaseModel):
    signal_id: str
    symbol: str
    side: str # BUY | SELL
    confidence: float
    size: float
    price: float
    stop: float
    target: float
    timestamp: int
    source: str

class TradingPlan(BaseModel):
    plan_id: str
    symbol: str
    strategy: str
    rules: List[str]
    backtest_stats: dict
    risk_metrics: dict
    human_readable_plan: str
