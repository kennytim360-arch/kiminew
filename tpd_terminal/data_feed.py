import requests
import os
import time
from dotenv import load_dotenv

load_dotenv()

class FinnhubDataFeed:
    def __init__(self):
        self.api_key = os.getenv('FINNHUB_API_KEY')
        if not self.api_key:
            raise ValueError("FINNHUB_API_KEY not found in .env file")
        self.base_url = "https://finnhub.io/api/v1"

    def get_candle_data(self, symbol, resolution='1'):
        """Get recent candle data with volume"""
        end_time = int(time.time())
        start_time = end_time - 3600  # Last hour

        url = f"{self.base_url}/stock/candle"
        params = {
            'symbol': symbol,
            'resolution': resolution,
            'from': start_time,
            'to': end_time,
            'token': self.api_key
        }
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        # Check if data is valid
        if data.get('s') != 'ok' or not data.get('c'):
            # Fallback to quote endpoint without volume
            quote_data = self.get_quote(symbol)
            # Add synthetic volume based on price movement
            quote_data['v'] = 1000  # Default volume
            return quote_data

        # Return latest candle in quote-like format
        return {
            'c': data['c'][-1],  # Close price
            'h': data['h'][-1],  # High
            'l': data['l'][-1],  # Low
            'o': data['o'][-1],  # Open
            'v': data['v'][-1] if data['v'][-1] else 1000,  # Volume
            't': data['t'][-1],  # Timestamp
            'pc': data['c'][-2] if len(data['c']) > 1 else data['c'][-1]  # Previous close
        }

    def get_quote(self, symbol):
        """Fallback quote endpoint (no volume)"""
        url = f"{self.base_url}/quote"
        params = {'symbol': symbol, 'token': self.api_key}
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        return response.json()

    def get_us500(self):
        # Use SPX for S&P 500 index
        return self.get_candle_data('SPX')

    def get_usdjpy(self):
        # Use OANDA format for forex
        return self.get_candle_data('OANDA:USD_JPY')

    def get_vix(self):
        # Use VIX symbol
        return self.get_candle_data('VIX')
