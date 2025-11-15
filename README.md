# Production-Grade AI Trading Engine

This project provides a production-grade AI trading engine that ingests live market data from Upstox, runs a modular AI/ML strategy, and serves live signals and trading plans via a secure FastAPI service.

## High-Level Architecture

```
┌─────────────────┐      ┌─────────────────┐      ┌─────────────────┐
│ Data Ingestor   │─────►│ Data Store      │─────►│ Feature Pipeline│
│ (Upstox)        │      │ (PostgreSQL)    │      │ (Incremental)   │
└─────────────────┘      └─────────────────┘      └─────────────────┘
        │                        │                        │
        ▼                        ▼                        ▼
┌─────────────────┐      ┌─────────────────┐      ┌─────────────────┐
│ Model Module(s) │─────►│ Backtester      │─────►│ Risk Manager    │
│ (ML/DL + Rules) │      │ & Simulator     │      │ & Position Sizing│
└─────────────────┘      └─────────────────┘      └─────────────────┘
        │                        │                        │
        ▼                        ▼                        ▼
┌─────────────────┐      ┌─────────────────┐      ┌─────────────────┐
│ Execution       │◄─────│ FastAPI Service │◄─────│ Monitoring &    │
│ Adapter (Stub)  │      │ (REST API)      │      │ Logging         │
└─────────────────┘      └─────────────────┘      └─────────────────┘
```

## Core Modules

- **`upstox_client.py`**: A robust client for the Upstox API, handling authentication, rate limiting, and data fetching.
- **`feature_store.py`**: A modular feature pipeline for incremental feature engineering (e.g., SMA, EMA, RSI).
- **`model_interface.py`**: A clear interface for ML models, with a training script in `train.py`.
- **`backtester.py`**: An event-driven simulator for backtesting and evaluating trading strategies.
- **`risk_manager.py`**: A module for position sizing, stop-loss handling, and other risk management tasks.
- **`api/main.py`**: A FastAPI application with endpoints for health checks, signals, trading plans, and execution.

## Getting Started

### Prerequisites

- Docker and Docker Compose
- Python 3.10+
- An Upstox API key and secret

### Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/your-repo.git
   cd your-repo
   ```

2. **Create a `.env` file** in the `trading_engine_v2` directory with the following content:
   ```
   UPSTOX_API_KEY=your_api_key
   UPSTOX_API_SECRET=your_api_secret
   UPSTOX_ACCESS_TOKEN=your_access_token
   DATABASE_URL=postgresql://user:password@postgres/trading_bot
   REDIS_URL=redis://redis:6379
   ```

3. **Build and run the application with Docker Compose:**
   ```bash
   cd trading_engine_v2
   docker-compose up --build
   ```

## API Endpoints

- **`GET /health`**: Returns the status of the application.
- **`GET /metrics`**: Exposes Prometheus-compatible metrics.
- **`GET /signals`**: Returns current live trading signals.
- **`GET /plans/{symbol}`**: Returns the latest trading plan for a given symbol.
- **`POST /execute`**: Executes a trading order.
- **`POST /override`**: Overrides the current trading strategy or risk parameters.
- **`GET /backtest/{strategy}`**: Triggers or fetches the results of a backtest.

## Disclaimer

This is a powerful trading engine. Use it at your own risk. The developers are not responsible for any financial losses. Always test your strategies thoroughly in a simulated environment before deploying with real capital.
