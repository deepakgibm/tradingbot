# Upstox Trading Bot - Project Documentation

## Overview

Full-stack intraday trading bot using LSTM machine learning and technical analysis. Built with FastAPI backend and React frontend, designed for simulated paper trading on Indian stocks.

## Project Structure

```
/
├── main.py                  # FastAPI application with WebSocket support
├── trading_engine.py        # Core trading logic and position management
├── ml_model.py             # LSTM neural network for price prediction
├── technical_indicators.py  # RSI, EMA, MACD, ATR calculations
├── market_simulator.py      # Simulated market data generator
├── database.py             # SQLite database for trades and logs
├── config.py               # Trading configuration parameters
├── requirements.txt        # Python dependencies
├── client/                 # React frontend
│   ├── src/
│   │   ├── App.tsx        # Main dashboard component
│   │   └── App.css        # Styling
│   ├── vite.config.ts     # Vite configuration with proxy
│   └── package.json       # Frontend dependencies
└── README.md              # User documentation
```

## Recent Changes

- **2025-11-13**: Initial project setup and configuration
  - Created FastAPI backend with trading engine
  - Implemented LSTM model for price prediction
  - Built React dashboard with real-time updates
  - Added WebSocket support for live data streaming
  - Configured simulated market data for 5 Indian stocks
  - Set up SQLite database for persistence
  - Fixed Vite allowedHosts configuration for Replit
  - Added backend workflow for continuous operation
  - Moved LSTM training to background task for faster startup

## User Preferences

- **Stack**: FastAPI (Python) + React (TypeScript)
- **Mode**: Simulated trading (paper trading)
- **Focus**: Educational/demonstration purposes
- **Architecture**: Backend (port 8000) + Frontend (port 5000)

## Key Features

1. **LSTM Machine Learning**: 60-minute lookback, 2-layer architecture
2. **Technical Analysis**: Multi-signal confirmation strategy
3. **Real-time Dashboard**: Live portfolio tracking and market data
4. **Risk Management**: Automated stop-loss and position sizing
5. **WebSocket Integration**: Real-time updates without polling

## Trading Configuration

Current parameters (in `config.py`):
- Capital: ₹2,00,000
- Risk per trade: 1%
- Max positions: 5
- Position size: 20% of capital
- Stop loss: 2x ATR
- Take profit: 2:1 risk-reward

## Technical Stack

**Backend**:
- FastAPI 0.104.1
- TensorFlow 2.15.0 (CPU-optimized)
- pandas 2.1.3
- numpy 1.26.2
- aiosqlite 0.19.0

**Frontend**:
- React 18 with TypeScript
- Vite 7.2.2
- Recharts (for future chart implementation)
- Native WebSocket API

## Deployment

- **Frontend**: Runs on port 5000 (workflow: frontend)
- **Backend**: Runs on port 8000 (workflow: backend)
- **Proxy**: Vite proxies /api and /ws to backend
- **WebSocket**: Supports both ws:// and wss:// protocols
- **Startup Time**: Backend takes 15-20 seconds to initialize (TensorFlow loading)

## Data Flow

1. Market Simulator generates realistic OHLCV data
2. Trading Engine analyzes signals using technical indicators + LSTM
3. Positions are managed with risk controls (stop-loss, take-profit)
4. Database stores all trades, positions, and logs
5. WebSocket broadcasts updates to frontend
6. React dashboard displays real-time portfolio and market data

## Next Steps

Future enhancements to consider:
1. Integrate live Upstox API (requires API keys)
2. Add GPU support for faster LSTM inference
3. Implement historical backtesting
4. Add advanced charting with Recharts
5. Create strategy optimizer
6. Add email/SMS notifications
7. Multi-timeframe analysis
8. Performance analytics dashboard

## Notes

- Currently in simulation mode (no real money)
- LSTM model is pre-trained on dummy data
- Market data updates every 2 seconds
- Trading signals checked every 5 seconds
- All data persists in SQLite database
