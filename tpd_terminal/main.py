#!/usr/bin/env python3
import time
import schedule
import yaml
import argparse
import sys
import os
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from data_feed import FinnhubDataFeed
from engine import TPDSignalEngine
from logger import TPDLogger

class TPDApp:
    def __init__(self, config_path='config.yaml'):
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)

        self.feed = FinnhubDataFeed()
        self.engine = TPDSignalEngine(self.config)
        self.logger = TPDLogger(self.config)

        # Create logs directory
        Path("logs").mkdir(exist_ok=True)

        self.running = False

    def job(self):
        """Main processing job"""
        try:
            us500 = self.feed.get_us500()
            usdjpy = self.feed.get_usdjpy()
            vix = self.feed.get_vix()

            if not all([us500, usdjpy, vix]):
                self.logger.log('WARNING', "Missing data from one or more feeds")
                return

            signal = self.engine.process_tick(us500, usdjpy, vix)

            if signal:
                self.logger.signal(signal)

            # Log status every 5 minutes
            if int(time.time()) % 300 == 0:
                self.logger.log('INFO', f"System running - Last price: {us500['c']:.2f}")

        except KeyError as e:
            import traceback
            self.logger.log('ERROR', f"Data key error: {str(e)}")
            self.logger.log('ERROR', f"Traceback: {traceback.format_exc()}")
        except Exception as e:
            import traceback
            self.logger.log('ERROR', f"Job error: {str(e)}")
            self.logger.log('ERROR', f"Traceback: {traceback.format_exc()}")

    def run(self):
        """Start the scheduler"""
        self.logger.log('INFO', "╔══════════════════════════════════════════════════════╗")
        self.logger.log('INFO', "║   TPD Signal Generator v2.0 - Terminal Mode          ║")
        self.logger.log('INFO', "║   Data Source: Finnhub (Free Tier)                   ║")
        self.logger.log('INFO', "╚══════════════════════════════════════════════════════╝")

        interval = self.config['data']['poll_interval_seconds']
        schedule.every(interval).seconds.do(self.job)

        self.logger.log('INFO', f"Polling interval: {interval} seconds")
        self.logger.log('INFO', "Press Ctrl+C to stop")

        self.running = True

        try:
            while self.running:
                schedule.run_pending()
                time.sleep(1)
        except KeyboardInterrupt:
            self.logger.log('INFO', "\nShutting down gracefully...")
            self.running = False
        except Exception as e:
            self.logger.log('ERROR', f"Fatal error: {e}")
            sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description='TPD Signal Generator')
    parser.add_argument('action', choices=['start', 'stop', 'status'],
                       help='Action to perform')
    args = parser.parse_args()

    if args.action == 'start':
        app = TPDApp()
        app.run()
    elif args.action == 'stop':
        print("To stop the running process, press Ctrl+C in the terminal where it's running")
    elif args.action == 'status':
        print("Check the log file: logs/tpd_signals.log")
        print("Or run: tail -f logs/tpd_signals.log")

if __name__ == '__main__':
    main()
