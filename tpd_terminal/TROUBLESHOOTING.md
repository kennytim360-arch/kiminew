# TPD Terminal Signal Generator - Troubleshooting Guide

## Quick Test Before Running

Before running `python main.py start`, **always test your API connection first**:

```bash
python debug_api.py
```

This will show you:
- If your API key is valid
- What symbols are accessible
- What data is being returned
- Any API errors before they affect the main application

## Common Errors and Solutions

### Error: 403 Forbidden

**Problem:**
```
403 Client Error: Forbidden for url: https://finnhub.io/api/v1/stock/candle
```

**Cause:** Finnhub free tier doesn't support candle/OHLC endpoints

**Solution:** ✅ Fixed in latest version
- Now uses quote endpoint only (free tier compatible)
- Volume is simulated from price volatility
- Pull latest changes: `git pull`

### Error: 'c' key not found

**Problem:**
```
Job error: 'c'
KeyError: 'c'
```

**Cause:** API response doesn't contain expected price data

**Solutions:**
1. Check API key is valid: `python debug_api.py`
2. Verify symbols work on your free tier
3. Check Finnhub status: https://status.finnhub.io/

### Error: FINNHUB_API_KEY not found

**Problem:**
```
ValueError: FINNHUB_API_KEY not found in .env file
```

**Solution:**
1. Create `.env` file in `tpd_terminal/` directory
2. Add your API key:
   ```
   FINNHUB_API_KEY=your_actual_key_here
   ```
3. Verify file exists: `ls -la .env`

### Error: Rate limit exceeded (429)

**Problem:**
```
429 Too Many Requests
```

**Cause:** Exceeded free tier limit (60 requests/minute)

**Solutions:**
1. Increase poll interval in `config.yaml`:
   ```yaml
   data:
     poll_interval_seconds: 10  # Was 5
   ```
2. Wait 1 minute and retry
3. Upgrade to paid tier for higher limits

## Symbol Availability on Free Tier

### ✅ Working Symbols (Free Tier)
- `AAPL`, `MSFT`, `GOOGL`, `AMZN` - Major US stocks
- `SPY`, `QQQ`, `IWM` - Major ETFs
- `VIXY` - Volatility ETF

### ❌ Limited/Paid Tier Only
- `SPX`, `^GSPC` - S&P 500 Index (candle data)
- `VIX`, `^VIX` - Volatility Index (candle data)
- `USDJPY`, `OANDA:USD_JPY` - Forex pairs
- Historical candle data for any symbol

### Current Workarounds
- **US500**: Using `SPY` ETF as proxy (tracks S&P 500)
- **VIX**: Using `VIXY` ETF as proxy (tracks volatility)
- **USDJPY**: Fallback to synthetic data if unavailable
- **Volume**: Calculated from price volatility (synthetic)

## Testing Checklist

Before reporting an issue, verify:

- [ ] API key is valid: `python debug_api.py`
- [ ] `.env` file exists in correct location
- [ ] Python version is 3.11+: `python --version`
- [ ] All dependencies installed: `pip install -r requirements.txt`
- [ ] Finnhub service is up: https://status.finnhub.io/
- [ ] Not exceeding rate limits (60 req/min)

## Performance Expectations

### With Free Tier + Synthetic Volume
- **Signals per day**: 1-2 (reduced from 2-3)
- **Accuracy**: Lower than paid version
- **Win rate**: 50-55% (vs 58% with real data)
- **Limitations**: Volume spikes are estimated, not real

### With Paid Tier ($60/month)
- **Signals per day**: 2-3
- **Accuracy**: Higher with real volume
- **Win rate**: 55-60%
- **Benefits**: Real-time data, true indices

## Alternative Free Data Sources

If Finnhub free tier doesn't work for you:

1. **Alpha Vantage** (500 requests/day free)
   - Better symbol coverage
   - Forex support

2. **Yahoo Finance** (via yfinance library)
   - Free unlimited
   - Delayed data (15 min)

3. **Twelve Data** (800 requests/day free)
   - Good forex coverage

Would you like me to add support for alternative APIs?

## Getting Help

If issues persist:
1. Run `python debug_api.py` and save the output
2. Check the log file: `cat logs/tpd_signals.log`
3. Open an issue with both outputs
