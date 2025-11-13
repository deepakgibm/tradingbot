from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import asyncio
import json
from typing import List, Dict, Any
from contextlib import asynccontextmanager

from config import config, TradingConfig
from database import db
from trading_engine import trading_engine
from market_simulator import market_sim
from ml_model import lstm_model

active_connections: List[WebSocket] = []

@asynccontextmanager
async def lifespan(app: FastAPI):
    await db.init_db()
    
    asyncio.create_task(initialize_model())
    asyncio.create_task(market_update_loop())
    asyncio.create_task(trading_loop())
    
    yield

async def initialize_model():
    await asyncio.to_thread(lstm_model.create_pretrained_model)

app = FastAPI(title="Upstox Trading Bot", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TradeRequest(BaseModel):
    symbol: str
    action: str

async def broadcast_message(message: Dict[str, Any]):
    if active_connections:
        message_str = json.dumps(message)
        for connection in active_connections:
            try:
                await connection.send_text(message_str)
            except:
                pass

async def market_update_loop():
    while True:
        market_sim.update_prices()
        await trading_engine.update_positions()
        
        portfolio = trading_engine.get_portfolio_summary()
        positions = [pos.to_dict() for pos in trading_engine.positions.values()]
        
        market_data = {}
        symbols_list = market_sim.get_all_symbols()
        for symbol_info in symbols_list:
            symbol = symbol_info['symbol']
            price_data = market_sim.get_current_price(symbol)
            market_data[symbol] = price_data
        
        await broadcast_message({
            "type": "portfolio_update",
            "data": {
                "portfolio": portfolio,
                "positions": positions,
                "market_data": market_data
            }
        })
        
        await asyncio.sleep(2)

async def trading_loop():
    while True:
        if trading_engine.is_running:
            symbols = market_sim.get_all_symbols()
            
            for symbol_info in symbols:
                symbol = symbol_info['symbol']
                
                try:
                    analysis = await trading_engine.analyze_signals(symbol)
                    
                    if analysis['action'] in ['BUY', 'SELL']:
                        result = await trading_engine.execute_trade(
                            symbol,
                            analysis['action'],
                            analysis['signals']
                        )
                        
                        if result['status'] == 'executed':
                            await broadcast_message({
                                "type": "trade_executed",
                                "data": result
                            })
                            
                            await db.add_log(
                                "TRADE",
                                f"{result['action']} {result['quantity']} {result['symbol']}",
                                result
                            )
                except Exception as e:
                    await db.add_log("ERROR", f"Error analyzing {symbol}: {str(e)}")
        
        await asyncio.sleep(5)

@app.get("/")
async def root():
    return {"status": "Trading Bot API is running", "simulation_mode": config.simulation_mode}

@app.get("/api/symbols")
async def get_symbols():
    return market_sim.get_all_symbols()

@app.get("/api/market/{symbol}")
async def get_market_data(symbol: str):
    return market_sim.get_current_price(symbol)

@app.get("/api/historical/{symbol}")
async def get_historical_data(symbol: str, days: int = 7):
    df = market_sim.get_historical_data(symbol, days)
    return {
        "symbol": symbol,
        "data": df.to_dict(orient='records')
    }

@app.get("/api/portfolio")
async def get_portfolio():
    portfolio = trading_engine.get_portfolio_summary()
    positions = [pos.to_dict() for pos in trading_engine.positions.values()]
    
    return {
        "portfolio": portfolio,
        "positions": positions
    }

@app.get("/api/signals/{symbol}")
async def get_signals(symbol: str):
    analysis = await trading_engine.analyze_signals(symbol)
    return analysis

@app.post("/api/trade")
async def execute_trade(trade: TradeRequest):
    analysis = await trading_engine.analyze_signals(trade.symbol)
    result = await trading_engine.execute_trade(trade.symbol, trade.action, analysis['signals'])
    return result

@app.get("/api/config")
async def get_config():
    return config.model_dump()

@app.post("/api/config")
async def update_config(new_config: TradingConfig):
    global config
    config = new_config
    return {"status": "updated", "config": config.model_dump()}

@app.post("/api/bot/start")
async def start_bot():
    trading_engine.is_running = True
    await db.add_log("INFO", "Trading bot started")
    return {"status": "started", "is_running": True}

@app.post("/api/bot/stop")
async def stop_bot():
    trading_engine.is_running = False
    await db.add_log("INFO", "Trading bot stopped")
    return {"status": "stopped", "is_running": False}

@app.get("/api/bot/status")
async def get_bot_status():
    return {
        "is_running": trading_engine.is_running,
        "simulation_mode": config.simulation_mode
    }

@app.get("/api/logs")
async def get_logs(limit: int = 100):
    logs = await db.get_recent_logs(limit)
    return logs

@app.get("/api/trades")
async def get_trades(limit: int = 100):
    trades = await db.get_trades(limit)
    return trades

@app.get("/api/performance")
async def get_performance():
    stats = await db.get_performance_stats()
    return stats

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    active_connections.append(websocket)
    
    try:
        portfolio = trading_engine.get_portfolio_summary()
        positions = [pos.to_dict() for pos in trading_engine.positions.values()]
        
        await websocket.send_text(json.dumps({
            "type": "initial_data",
            "data": {
                "portfolio": portfolio,
                "positions": positions,
                "symbols": market_sim.get_all_symbols(),
                "is_running": trading_engine.is_running
            }
        }))
        
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)
            
            if message.get('type') == 'ping':
                await websocket.send_text(json.dumps({"type": "pong"}))
    
    except WebSocketDisconnect:
        active_connections.remove(websocket)
    except Exception as e:
        if websocket in active_connections:
            active_connections.remove(websocket)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
