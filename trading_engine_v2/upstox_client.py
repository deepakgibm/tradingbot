import os
import time
import logging
import requests
from typing import Callable, List, Dict, Any
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class UpstoxClient:
    """
    A robust client for the Upstox API.
    Handles authentication, rate limiting, and provides methods for
    fetching data and placing orders.
    """

    def __init__(self):
        self.api_key = os.getenv("UPSTOX_API_KEY")
        self.api_secret = os.getenv("UPSTOX_API_SECRET")
        self.access_token = os.getenv("UPSTOX_ACCESS_TOKEN")
        self.base_url = "https://api.upstox.com/v2"
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {self.access_token}",
            "Accept": "application/json"
        })

    def _request(self, method: str, endpoint: str, params: Dict[str, Any] = None, data: Dict[str, Any] = None):
        """
        A helper method to handle API requests with rate limiting and error handling.
        """
        url = f"{self.base_url}{endpoint}"
        while True:
            try:
                response = self.session.request(method, url, params=params, json=data)
                response.raise_for_status()
                return response.json()
            except requests.exceptions.HTTPError as e:
                if e.response.status_code == 429:
                    retry_after = int(e.response.headers.get("Retry-After", 1))
                    logging.warning(f"Rate limit exceeded. Retrying in {retry_after} seconds.")
                    time.sleep(retry_after)
                else:
                    logging.error(f"HTTP error: {e}")
                    return None
            except requests.exceptions.RequestException as e:
                logging.error(f"Request error: {e}")
                return None

    def get_instrument_master(self) -> List[Dict[str, Any]]:
        """
        Fetches the instrument master from Upstox.
        """
        logging.info("Fetching instrument master.")
        return self._request("GET", "/instrument/master")

    def fetch_historical(self, symbol: str, start_ts: str, end_ts: str, timeframe: str) -> List[Dict[str, Any]]:
        """
        Fetches historical OHLC/candle data for a given symbol.
        """
        logging.info(f"Fetching historical data for {symbol} from {start_ts} to {end_ts}.")
        params = {
            "instrument_key": symbol,
            "interval": timeframe,
            "from_date": start_ts,
            "to_date": end_ts
        }
        return self._request("GET", "/historical-candle", params=params)

    def subscribe_ticks(self, symbols: List[str], on_tick_cb: Callable):
        """
        Subscribes to live ticks using a WebSocket connection.
        (This is a placeholder for the WebSocket implementation)
        """
        logging.info(f"Subscribing to ticks for {symbols}.")
        # WebSocket implementation would go here
        pass

    def poll_ticks(self, symbols: List[str], on_tick_cb: Callable):
        """
        Polls for live ticks using REST API calls with exponential backoff.
        """
        logging.info(f"Polling ticks for {symbols}.")
        # Polling implementation would go here
        pass

    def place_order(self, order_spec: Dict[str, Any]) -> Dict[str, Any]:
        """
        Places an order with the given specifications.
        (This is a stub and does not execute real orders)
        """
        logging.info(f"Placing order: {order_spec}")
        # In a real implementation, this would make a POST request to the order placement endpoint
        return {"status": "success", "order_id": "mock_order_123"}

    def get_order_status(self, order_id: str) -> Dict[str, Any]:
        """
        Gets the status of an order.
        (This is a stub)
        """
        logging.info(f"Getting status for order {order_id}")
        return {"status": "completed", "order_id": order_id}
