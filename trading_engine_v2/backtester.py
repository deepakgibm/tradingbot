import pandas as pd
from typing import List, Dict, Any

class Backtester:
    """
    An event-driven simulator for backtesting trading strategies.
    """

    def __init__(self, strategy, capital: float = 100000.0, commission: float = 0.001, slippage: float = 0.001):
        self.strategy = strategy
        self.initial_capital = capital
        self.capital = capital
        self.commission = commission
        self.slippage = slippage
        self.positions: Dict[str, float] = {}
        self.history: List[Dict[str, Any]] = []

    def run(self, data: pd.DataFrame):
        """
        Runs the backtest on the given historical data.
        """
        for i, row in data.iterrows():
            signal = self.strategy.generate_signal(row)

            if signal:
                self._execute_signal(signal, row)

            self._update_portfolio(row)

        return self._calculate_metrics()

    def _execute_signal(self, signal: Dict[str, Any], current_data: pd.Series):
        """
        Executes a trading signal, accounting for commission and slippage.
        """
        symbol = signal["symbol"]
        side = signal["side"]
        size = signal["size"]
        price = current_data["close"]

        # Apply slippage
        if side == "BUY":
            price *= (1 + self.slippage)
        else:
            price *= (1 - self.slippage)

        cost = size * price
        commission_cost = cost * self.commission

        if side == "BUY" and self.capital >= cost + commission_cost:
            self.capital -= (cost + commission_cost)
            self.positions[symbol] = self.positions.get(symbol, 0) + size
            self._record_trade(symbol, "BUY", size, price, commission_cost)
        elif side == "SELL" and self.positions.get(symbol, 0) >= size:
            self.capital += (cost - commission_cost)
            self.positions[symbol] -= size
            self._record_trade(symbol, "SELL", size, price, commission_cost)

    def _update_portfolio(self, current_data: pd.Series):
        """
        Updates the portfolio value based on the current market data.
        """
        portfolio_value = self.capital
        for symbol, size in self.positions.items():
            if symbol in current_data:
                portfolio_value += size * current_data[symbol]

        self.history.append({"timestamp": current_data.name, "portfolio_value": portfolio_value})

    def _record_trade(self, symbol: str, side: str, size: float, price: float, commission: float):
        """
        Records the details of a trade.
        """
        self.history.append({
            "timestamp": pd.Timestamp.now(),
            "symbol": symbol,
            "side": side,
            "size": size,
            "price": price,
            "commission": commission
        })

    def _calculate_metrics(self) -> Dict[str, Any]:
        """
        Calculates and returns the backtest performance metrics.
        """
        if not self.history:
            return {}

        portfolio_history = pd.DataFrame(self.history)
        portfolio_history["returns"] = portfolio_history["portfolio_value"].pct_change()

        sharpe_ratio = (portfolio_history["returns"].mean() / portfolio_history["returns"].std()) * (252**0.5)
        max_drawdown = (portfolio_history["portfolio_value"].cummax() - portfolio_history["portfolio_value"]).max()

        return {
            "sharpe_ratio": sharpe_ratio,
            "max_drawdown": max_drawdown,
            "final_capital": self.capital,
            "equity_curve": self.history
        }
