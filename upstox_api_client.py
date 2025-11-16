import os
import upstox_client
import logging
from upstox_client.rest import ApiException
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class UpstoxClient:
    def __init__(self):
        self.api_key = os.getenv("UPSTOX_API_KEY")
        self.api_secret = os.getenv("UPSTOX_API_SECRET")
        self.redirect_uri = os.getenv("UPSTOX_REDIRECT_URI")
        self.access_token = os.getenv("UPSTOX_ACCESS_TOKEN")
        self.api_client = None
        self._configure_api_client()

    def _configure_api_client(self):
        logging.info("Configuring Upstox API client.")
        configuration = upstox_client.Configuration()
        configuration.access_token = self.access_token
        self.api_client = upstox_client.ApiClient(configuration)

    def get_profile(self):
        logging.info("Fetching user profile from Upstox.")
        if not self.api_client:
            return {"status": "error", "message": "API client not configured."}
        try:
            user_api = upstox_client.UserApi(self.api_client)
            profile = user_api.get_profile(api_version="v2")
            return {"status": "success", "data": profile}
        except ApiException as e:
            logging.error(f"Upstox API exception while fetching profile: {e}")
            return {"status": "error", "message": str(e)}

    def get_funds_and_margin(self):
        logging.info("Fetching funds and margin from Upstox.")
        if not self.api_client:
            return {"status": "error", "message": "API client not configured."}
        try:
            user_api = upstox_client.UserApi(self.api_client)
            funds = user_api.get_user_fund_margin(api_version="v2")
            return {"status": "success", "data": funds}
        except ApiException as e:
            logging.error(f"Upstox API exception while fetching funds and margin: {e}")
            return {"status": "error", "message": str(e)}

    def get_historical_candle_data(self, instrument_key, interval, to_date, from_date):
        logging.info(f"Fetching historical data for {instrument_key} from {from_date} to {to_date}.")
        if not self.api_client:
            return {"status": "error", "message": "API client not configured."}
        try:
            history_api = upstox_client.HistoryApi(self.api_client)
            data = history_api.get_historical_candle_data(instrument_key, interval, to_date, from_date, api_version="v2")
            return {"status": "success", "data": data}
        except ApiException as e:
            logging.error(f"Upstox API exception while fetching historical data: {e}")
            return {"status": "error", "message": str(e)}

    def place_order(self, order_details):
        logging.info(f"Placing order: {order_details}")
        if not self.api_client:
            return {"status": "error", "message": "API client not configured."}
        try:
            order_api = upstox_client.OrderApi(self.api_client)
            order_response = order_api.place_order(body=order_details, api_version="v2")
            return {"status": "success", "data": order_response}
        except ApiException as e:
            logging.error(f"Upstox API exception while placing order: {e}")
            return {"status": "error", "message": str(e)}

    def cancel_order(self, order_id):
        logging.info(f"Cancelling order: {order_id}")
        if not self.api_client:
            return {"status": "error", "message": "API client not configured."}
        try:
            order_api = upstox_client.OrderApi(self.api_client)
            order_response = order_api.cancel_order(order_id, api_version="v2")
            return {"status": "success", "data": order_response}
        except ApiException as e:
            logging.error(f"Upstox API exception while cancelling order: {e}")
            return {"status": "error", "message": str(e)}

upstox_client_instance = UpstoxClient()
