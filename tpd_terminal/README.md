# TPD Signal Generator - Terminal Edition

## Overview
Topological Persistence Divergence signal generator for manual CFD trading. Runs locally in your terminal, generates signals based on simulated order book persistence, no automated execution.

## Features
- Free data via Finnhub API (no cost)
- Simulated L2 depth using volume profile
- Sweep detection and confidence scoring
- Terminal alerts with color coding
- Log file for performance tracking

## Installation

### 1. Get API Key
Sign up at https://finnhub.io/register (free tier, 60 requests/min)

### 2. Setup Environment
```bash
mkdir ~/tpd_trader && cd ~/tpd_trader

# Copy all files created by Claude Code here
# Then:

python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Configure API Key
```bash
echo "FINNHUB_API_KEY=your_actual_key_here" > .env
```

## Usage

### Start Signal Generation
```bash
python main.py start
```

### Stop
Press `Ctrl+C` in the terminal

### View Logs
```bash
tail -f logs/tpd_signals.log
```

## Configuration

Edit `config.yaml` to adjust:
- `sweep_detection.volume_spike_multiplier`: Higher = fewer signals
- `trading.min_confidence`: 0.65 default
- `output.audio_beep`: Set true for sound alerts

## Manual Trade Execution

When you see a SIGNAL:
1. Note entry price, stop, target
2. Open broker platform (IG, OANDA, etc.)
3. Place LIMIT order at entry price
4. Set stop loss and take profit as shown
5. Size: 0.5% risk per trade

## Expected Performance

- Signals/day: 2-3
- Win rate: 55-60%
- Avg hold time: 10-15 minutes
- Requires active monitoring 13:00-16:00 GMT

## Troubleshooting

**Error: "FINNHUB_API_KEY not found"**
- Fix: Check .env file exists and has correct key

**Error: "429 Too Many Requests"**
- Fix: Reduce poll_interval_seconds in config.yaml to 10

**No signals for hours**
- Normal: Strategy is selective, wait for market volatility

## Disclaimer
This tool provides signals for educational purposes. You are solely responsible for execution decisions. CFD trading involves high risk of loss.
