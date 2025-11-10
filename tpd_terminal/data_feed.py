import requests
import os
from dotenv import load_dotenv

load_dotenv()

class FinnhubDataFeed:
    def __init__(self):
        self.api_key = os.getenv('FINNHUB_API_KEY')
        if not self.api_key:
            raise ValueError("FINNHUB_API_KEY not found in .env file")
        self.base_url = "https://finnhub.io/api/v1"

    def get_quote(self, symbol):
        url = f"{self.base_url}/quote"
        params = {'symbol': symbol, 'token': self.api_key}
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        return response.json()

    def get_us500(self):
        return self.get_quote('^GSPC')

    def get_usdjpy(self):
        return self.get_quote('USDJPY')

    def get_vix(self):
        return self.get_quote('^VIX')
