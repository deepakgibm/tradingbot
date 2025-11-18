# Tech Stack
Use fastAPI for backend and React for frontend
# Upstox Intraday Trading Bot with Machine Learning

A full-stack trading bot application that combines LSTM neural networks with technical analysis to execute simulated intraday trades on the Indian stock market.

## Features

- **LSTM Machine Learning**: Price prediction using TensorFlow/Keras with 60-minute lookback
- **Technical Indicators**: RSI, EMA, MACD, ATR calculations for signal confirmation
- **Multi-Signal Strategy**: Requires 3 out of 4 signals for trade execution
- **Real-time Dashboard**: React-based UI with live portfolio tracking and WebSocket updates
- **Risk Management**: Dynamic position sizing, stop-loss, and take-profit automation
- **Simulated Trading**: Paper trading mode with realistic market simulation

## Tech Stack

### Backend
- FastAPI (Python 3.13)
- TensorFlow/Keras for LSTM model
- pandas + numpy for data processing
- SQLite for data persistence
- WebSockets for real-time communication

### Frontend
- React with TypeScript
- Vite for fast development
- WebSocket client for live updates
- Responsive modern UI

## Getting Started

The application is already configured and running on Replit. Simply:

1. **Start the Trading Bot**: Click the "Start Bot" button in the dashboard
2. **Monitor Portfolio**: View real-time P&L, positions, and market data
3. **Adjust Settings**: Modify trading parameters in `config.py`

### Manual Setup

If running locally:

```bash
# Backend
pip install -r requirements.txt
python main.py

# Frontend (in another terminal)
cd client
npm install
npm run dev
```

## Configuration

Edit `config.py` to adjust trading parameters:

```python
capital = 200000.0              # Starting capital
max_risk_per_trade = 0.01       # 1% risk per trade
max_positions = 5               # Maximum concurrent positions
rsi_oversold = 30               # RSI oversold threshold
rsi_overbought = 70             # RSI overbought threshold
```

## Trading Strategy

### Entry Signals (Need 3 of 4)
1. RSI < 30 (Oversold)
2. EMA(20) > EMA(50) (Uptrend)
3. MACD > Signal Line (Bullish momentum)
4. LSTM predicts > 0.5% upside

### Exit Signals (Need 3 of 4)
1. RSI > 70 (Overbought)
2. EMA(20) < EMA(50) (Downtrend)
3. MACD < Signal Line (Bearish momentum)
4. LSTM predicts > 0.5% downside

### Risk Management
- **Position Sizing**: 20% of capital per trade
- **Stop Loss**: 2x ATR from entry price
- **Take Profit**: 2:1 risk-reward ratio
- **Maximum Loss**: Circuit breaker at 5% daily loss

## API Endpoints

- `GET /api/portfolio` - Portfolio summary and positions
- `GET /api/symbols` - Available trading symbols
- `GET /api/market/{symbol}` - Current market data
- `GET /api/signals/{symbol}` - Trading signals analysis
- `POST /api/bot/start` - Start trading bot
- `POST /api/bot/stop` - Stop trading bot
- `GET /api/logs` - Trading logs
- `GET /api/trades` - Trade history
- `WebSocket /ws` - Real-time updates

## Simulated Stocks

The bot trades these Indian stocks in simulation mode:
- INFY (Infosys)
- RELIANCE (Reliance Industries)
- TCS (Tata Consultancy Services)
- HDFCBANK (HDFC Bank)
- ICICIBANK (ICICI Bank)

## Performance Monitoring

The dashboard displays:
- **Total Value**: Combined capital + position value
- **Total P&L**: Realized + unrealized profit/loss
- **Return %**: Percentage return on capital
- **Active Positions**: Current open trades
- **Market Overview**: Real-time stock prices

## Architecture

```
┌─────────────────┐         WebSocket         ┌──────────────────┐
│  React Frontend │◄──────────────────────────►│  FastAPI Backend │
│  (Port 5000)    │         REST API           │   (Port 8000)    │
└─────────────────┘                            └──────────────────┘
                                                        │
                                                        ├── Trading Engine
                                                        ├── LSTM Model
                                                        ├── Technical Indicators
                                                        ├── Market Simulator
                                                        └── SQLite Database
```

## Disclaimer

**This is a simulated trading bot for educational purposes only.**

- Past performance does not guarantee future results
- Trading involves substantial risk of loss
- Never risk money you cannot afford to lose
- Test thoroughly before any real trading
- Comply with all applicable laws and regulations

## Future Enhancements

- Live Upstox API integration
- GPU acceleration support
- Advanced charting with historical data
- Backtesting capabilities
- Email/SMS notifications
- Multi-timeframe analysis
- Portfolio optimization algorithms

## License

#Production readiness

To use this system with real trades, the following must be implemented:

Upstox OAuth2 Authentication

Implement authorization code flow
Token refresh mechanism
Session management
Real API Integration

Replace simulated data in server/upstox.ts
Implement actual REST API calls to api.upstox.com
Add WebSocket for real-time market data
Handle rate limiting and API errors
Order & Position Synchronization

Reconcile orders with broker state
Sync positions from Upstox
Handle partial fills
Implement order status tracking
Production Safety

Database persistence (replace in-memory storage)
Comprehensive error handling
Logging and monitoring
Backtesting framework
Paper trading mode
