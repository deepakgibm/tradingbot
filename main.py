from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request, Depends
from fastapi.responses import RedirectResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import asyncio
import structlog
from typing import List, Dict, Any
from contextlib import asynccontextmanager
from fastapi.security import OAuth2PasswordRequestForm

from config import config, TradingConfig
from database import db
from trading_engine import trading_engine
from upstox_api_client import upstox_client_instance
from ml_model import lstm_model
from auth import create_access_token, get_current_user
from logging_config import setup_logging

# Configure logging
setup_logging()
log = structlog.get_logger()

active_connections: List[WebSocket] = []

@asynccontextmanager
async def lifespan(app: FastAPI):
    await db.init_db()
    log.info("Database initialized.")
    
    asyncio.create_task(initialize_model())
    asyncio.create_task(trading_loop())
    
    yield

async def initialize_model():
    log.info("Initializing LSTM model...")
    await asyncio.to_thread(lstm_model.create_pretrained_model)
    log.info("LSTM model initialized.")

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
    log.error("Unhandled exception", exc_info=True)
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
            log.info("Trading loop is running...")
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
                    log.error("Error analyzing symbol", symbol=symbol, error=e, exc_info=True)
                    await db.add_log("ERROR", f"Error analyzing {symbol}: {str(e)}")
        
        await asyncio.sleep(5)

@app.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    # In a real application, you would verify the username and password against a database
    if form_data.username == "test" and form_data.password == "test":
        access_token = create_access_token(data={"sub": form_data.username})
        return {"access_token": access_token, "token_type": "bearer"}
    return JSONResponse(status_code=400, content={"message": "Incorrect username or password"})


@app.get("/auth/login")
async def login():
    try:
        login_url = upstox_client_instance.get_login_url()
        log.info("Redirecting to Upstox for authentication.")
        return RedirectResponse(url=login_url)
    except Exception as e:
        log.error("Failed to get login URL", error=e, exc_info=True)
        return {"status": "error", "message": "Failed to initiate login."}

@app.get("/auth/callback")
async def auth_callback(code: str):
    try:
        response = upstox_client_instance.handle_auth_callback(code)
        if response['status'] == 'success':
            log.info("Successfully authenticated with Upstox.")
            return {"status": "success", "message": "Authentication successful!"}
        else:
            log.error("Upstox authentication failed", message=response.get('message'))
            return {"status": "error", "message": "Authentication failed."}
    except Exception as e:
        log.error("Authentication callback error", error=e, exc_info=True)
        return {"status": "error", "message": "Authentication failed."}

@app.get("/")
async def root():
    return {"status": "Trading Bot API is running"}

@app.get("/api/portfolio")
async def get_portfolio(current_user: str = Depends(get_current_user)):
    portfolio = trading_engine.get_portfolio_summary()
    return portfolio

@app.post("/api/bot/start")
async def start_bot(current_user: str = Depends(get_current_user)):
    trading_engine.is_running = True
    log.info("Trading bot started.")
    await db.add_log("INFO", "Trading bot started")
    return {"status": "started", "is_running": True}

@app.post("/api/bot/stop")
async def stop_bot(current_user: str = Depends(get_current_user)):
    trading_engine.is_running = False
    log.info("Trading bot stopped.")
    await db.add_log("INFO", "Trading bot stopped")
    return {"status": "stopped", "is_running": False}

@app.get("/api/bot/status")
async def get_bot_status(current_user: str = Depends(get_current_user)):
    return {
        "is_running": trading_engine.is_running,
    }

@app.get("/api/historical-data/{instrument_key}")
async def get_historical_data(instrument_key: str, current_user: str = Depends(get_current_user)):
    today = date.today()
    from_date = today.replace(day=today.day - 7).strftime('%Y-%m-%d')
    to_date = today.strftime('%Y-%m-%d')

    historical_data = upstox_client_instance.get_historical_candle_data(
        instrument_key, '1minute', to_date, from_date
    )

    if historical_data['status'] != 'success' or not historical_data['data'].payload.candles:
        return {"error": "Could not fetch historical data"}

    return historical_data['data'].payload.candles

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
