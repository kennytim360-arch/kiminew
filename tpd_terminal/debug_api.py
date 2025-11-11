#!/usr/bin/env python3
"""Simple debug script to test Finnhub API connection"""
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from data_feed import FinnhubDataFeed
import json

print("Testing Finnhub API connection...")
print("=" * 60)

try:
    feed = FinnhubDataFeed()
    print("✓ API key loaded successfully")
    print()

    print("Fetching US500 (SPY/AAPL proxy) data...")
    us500 = feed.get_us500()
    print(f"US500 Response: {json.dumps(us500, indent=2)}")
    print()

    print("Fetching USDJPY data...")
    usdjpy = feed.get_usdjpy()
    print(f"USDJPY Response: {json.dumps(usdjpy, indent=2)}")
    print()

    print("Fetching VIX (VIXY proxy) data...")
    vix = feed.get_vix()
    print(f"VIX Response: {json.dumps(vix, indent=2)}")
    print()

    print("=" * 60)
    print("✓ All API calls successful!")
    print()
    print("Data summary:")
    print(f"  US500 Price: {us500.get('c', 'N/A')}")
    print(f"  US500 Volume (synthetic): {us500.get('v', 'N/A')}")
    print(f"  USDJPY Price: {usdjpy.get('c', 'N/A')}")
    print(f"  USDJPY Volume (synthetic): {usdjpy.get('v', 'N/A')}")
    print(f"  VIX Price: {vix.get('c', 'N/A')}")
    print(f"  VIX Volume (synthetic): {vix.get('v', 'N/A')}")
    print()
    print("Note: Volume is simulated based on price volatility")
    print("      (Finnhub free tier doesn't provide real volume data)")

except ValueError as e:
    print(f"✗ Configuration error: {e}")
    print("\nMake sure you have a .env file with your FINNHUB_API_KEY")
except Exception as e:
    import traceback
    print(f"✗ Error: {e}")
    print(f"\nFull traceback:")
    print(traceback.format_exc())
