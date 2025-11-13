from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request
from fastapi.responses import RedirectResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import asyncio
import json
import logging
from typing import List, Dict, Any
from contextlib import asynccontextmanager

from config import config, TradingConfig
from database import db
from trading_engine import trading_engine
from upstox_client import upstox_client_instance
from ml_model import lstm_model

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

active_connections: List[WebSocket] = []

@asynccontextmanager
async def lifespan(app: FastAPI):
    await db.init_db()
    logging.info("Database initialized.")
    
    asyncio.create_task(initialize_model())
    asyncio.create_task(trading_loop())
    
    yield

async def initialize_model():
    logging.info("Initializing LSTM model...")
    await asyncio.to_thread(lstm_model.create_pretrained_model)
    logging.info("LSTM model initialized.")

app = FastAPI(title="Upstox Trading Bot", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    logging.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"message": "An unexpected error occurred."}
    )

class TradeRequest(BaseModel):
    symbol: str
    action: str
    instrument_key: str

async def broadcast_message(message: Dict[str, Any]):
    if active_connections:
        message_str = json.dumps(message)
        for connection in active_connections:
            try:
                await connection.send_text(message_str)
            except:
                pass

async def trading_loop():
    while True:
        if trading_engine.is_running:
            logging.info("Trading loop is running...")
            # This will need to be updated with a list of instruments from Upstox
            symbols = []
            
            for symbol_info in symbols:
                symbol = symbol_info['symbol']
                instrument_key = symbol_info['instrument_key']
                
                try:
                    analysis = await trading_engine.analyze_signals(symbol, instrument_key)
                    
                    if analysis['action'] in ['BUY', 'SELL']:
                        result = await trading_engine.execute_trade(
                            symbol,
                            instrument_key,
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
                    logging.error(f"Error analyzing {symbol}: {e}", exc_info=True)
                    await db.add_log("ERROR", f"Error analyzing {symbol}: {str(e)}")
        
        await asyncio.sleep(5)

@app.get("/auth/login")
async def login():
    try:
        login_url = upstox_client_instance.get_login_url()
        logging.info("Redirecting to Upstox for authentication.")
        return RedirectResponse(url=login_url)
    except Exception as e:
        logging.error(f"Failed to get login URL: {e}", exc_info=True)
        return {"status": "error", "message": "Failed to initiate login."}

@app.get("/auth/callback")
async def auth_callback(code: str):
    try:
        response = upstox_client_instance.handle_auth_callback(code)
        if response['status'] == 'success':
            logging.info("Successfully authenticated with Upstox.")
            return {"status": "success", "message": "Authentication successful!"}
        else:
            logging.error(f"Upstox authentication failed: {response.get('message')}")
            return {"status": "error", "message": "Authentication failed."}
    except Exception as e:
        logging.error(f"Authentication callback error: {e}", exc_info=True)
        return {"status": "error", "message": "Authentication failed."}

@app.get("/")
async def root():
    return {"status": "Trading Bot API is running"}

@app.get("/api/portfolio")
async def get_portfolio():
    portfolio = trading_engine.get_portfolio_summary()
    return portfolio

@app.post("/api/bot/start")
async def start_bot():
    trading_engine.is_running = True
    logging.info("Trading bot started.")
    await db.add_log("INFO", "Trading bot started")
    return {"status": "started", "is_running": True}

@app.post("/api/bot/stop")
async def stop_bot():
    trading_engine.is_running = False
    logging.info("Trading bot stopped.")
    await db.add_log("INFO", "Trading bot stopped")
    return {"status": "stopped", "is_running": False}

@app.get("/api/bot/status")
async def get_bot_status():
    return {
        "is_running": trading_engine.is_running,
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
