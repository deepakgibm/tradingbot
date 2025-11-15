from typing import Dict, Any

class RiskManager:
    """
    Manages risk for the trading bot, including position sizing,
    stop-loss handling, and exposure limits.
    """

    def __init__(self, capital: float, risk_per_trade: float = 0.01, max_exposure: float = 0.2):
        self.capital = capital
        self.risk_per_trade = risk_per_trade
        self.max_exposure = max_exposure

    def size_position(self, entry_price: float, stop_loss_price: float) -> float:
        """
        Calculates the position size based on the risk per trade.
        """
        risk_amount = self.capital * self.risk_per_trade
        risk_per_share = abs(entry_price - stop_loss_price)
        if risk_per_share == 0:
            return 0
        return risk_amount / risk_per_share

    def check_exposure(self, new_position_value: float, current_exposure: float) -> bool:
        """
        Checks if a new position would exceed the maximum exposure limit.
        """
        return (current_exposure + new_position_value) / self.capital <= self.max_exposure

    def manage_signal(self, signal: Dict[str, Any]) -> Dict[str, Any]:
        """
        Consumes a trading signal and returns an order specification with risk management applied,
        or vetoes the signal.
        """
        entry_price = signal.get("price")
        stop_loss_price = signal.get("stop")

        if not entry_price or not stop_loss_price:
            return {"action": "veto", "reason": "Missing price or stop loss"}

        position_size = self.size_position(entry_price, stop_loss_price)
        position_value = position_size * entry_price

        # Assuming a function to get current total exposure
        current_exposure = self._get_current_exposure()
        if not self.check_exposure(position_value, current_exposure):
            return {"action": "veto", "reason": "Exceeds maximum exposure"}

        order_spec = {
            "symbol": signal["symbol"],
            "side": signal["side"],
            "size": position_size,
            "price": entry_price,
            "stop_loss": stop_loss_price,
            "take_profit": signal.get("target"),
        }

        return {"action": "place_order", "order_spec": order_spec}

    def _get_current_exposure(self) -> float:
        """
        A placeholder for a function that would return the current total exposure.
        In a real implementation, this would fetch data from a portfolio manager.
        """
        return 0.0
