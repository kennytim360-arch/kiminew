#!/usr/bin/env python3
"""Test script to check Finnhub API response format"""
import os
from dotenv import load_dotenv
import requests
import json

load_dotenv()

api_key = os.getenv('FINNHUB_API_KEY')
if not api_key:
    print("ERROR: FINNHUB_API_KEY not found in .env file")
    exit(1)

base_url = "https://finnhub.io/api/v1"

# Test different symbols
symbols = ['^GSPC', 'SPX', 'USDJPY', '^VIX', 'VIX']

print("Testing Finnhub API responses...")
print("=" * 60)

for symbol in symbols:
    print(f"\nSymbol: {symbol}")
    try:
        url = f"{base_url}/quote"
        params = {'symbol': symbol, 'token': api_key}
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        print(f"Response: {json.dumps(data, indent=2)}")
    except Exception as e:
        print(f"Error: {e}")

print("\n" + "=" * 60)
print("\nTesting candles endpoint for volume data...")
print("=" * 60)

# Test candles endpoint which has volume
import time
end_time = int(time.time())
start_time = end_time - 86400  # Last 24 hours

for symbol in ['SPX', 'AAPL']:  # Test with SPX and a stock
    print(f"\nSymbol: {symbol}")
    try:
        url = f"{base_url}/stock/candle"
        params = {
            'symbol': symbol,
            'resolution': '5',  # 5 minute candles
            'from': start_time,
            'to': end_time,
            'token': api_key
        }
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        print(f"Response keys: {data.keys()}")
        if 'v' in data:
            print(f"Volume data available: {len(data['v'])} points")
            print(f"Latest volume: {data['v'][-1] if data['v'] else 'None'}")
    except Exception as e:
        print(f"Error: {e}")
