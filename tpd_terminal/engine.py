import time
import numpy as np
from collections import deque

class SweepDetector:
    def __init__(self, config):
        self.config = config
        self.volume_history = deque(maxlen=12)

    def detect(self, current_volume):
        self.volume_history.append(current_volume)

        if len(self.volume_history) < 12:
            return {'is_sweep': False, 'impact': 0.0}

        avg_volume = np.mean(list(self.volume_history)[:-1])
        current_vol = self.volume_history[-1]

        if avg_volume == 0:
            return {'is_sweep': False, 'impact': 0.0}

        spike_ratio = current_vol / avg_volume

        if spike_ratio > self.config['sweep_detection']['volume_spike_multiplier']:
            impact = min(spike_ratio / 10.0, 0.6)
            return {'is_sweep': True, 'impact': impact}

        return {'is_sweep': False, 'impact': 0.0}

class TPDSignalEngine:
    def __init__(self, config):
        self.config = config
        self.sweep_detector = SweepDetector(config)
        self.price_history = deque(maxlen=30)
        self.correlation_history = deque(maxlen=20)

    def process_tick(self, us500_data, usdjpy_data, vix_data):
        current_price = us500_data['c']
        current_volume = us500_data['v']
        self.price_history.append(current_price)

        sweep = self.sweep_detector.detect(current_volume)

        if not sweep['is_sweep']:
            return None

        market_conditions = {
            'vix': vix_data['c'],
            'lyapunov': self.calculate_lyapunov(),
            'correlation': self.calculate_correlation(us500_data, usdjpy_data)
        }

        confidence = self.calculate_confidence(sweep, market_conditions)

        if confidence >= self.config['trading']['min_confidence']:
            return self.generate_signal(current_price, sweep['impact'], confidence)

        return None

    def calculate_lyapunov(self):
        if len(self.price_history) < 10:
            return 0.0
        returns = np.diff(list(self.price_history)) / list(self.price_history)[:-1]
        if len(returns) == 0:
            return 0.0
        return np.std(returns) * np.sqrt(252)  # Simplified proxy

    def calculate_correlation(self, us500, usdjpy):
        self.correlation_history.append({
            'us500': us500['c'],
            'usdjpy': usdjpy['c']
        })

        if len(self.correlation_history) < 10:
            return 0.8  # Default healthy correlation

        df = np.array([[x['us500'], x['usdjpy']] for x in self.correlation_history])
        corr = np.corrcoef(df[:, 0], df[:, 1])[0, 1]
        return corr if not np.isnan(corr) else 0.8

    def calculate_confidence(self, sweep, market):
        score = 0.0
        score += sweep['impact'] * 0.30

        if market['lyapunov'] > 0.4:
            score += 0.30

        vix = market['vix']
        if 12 <= vix <= 25:
            score += 0.20
        elif vix <= 35:
            score += 0.10

        correlation = market['correlation']
        if correlation > 0.65:
            score += 0.20
        elif correlation > 0.50:
            score += 0.10

        return min(score, 1.0)

    def generate_signal(self, price, impact, confidence):
        stop_distance = self.config['trading']['stop_base'] * (1 + impact / 2)
        stop_distance = min(stop_distance, 0.0055)

        stop_price = price * (1 - stop_distance)
        target_price = price + (price - stop_price) * self.config['trading']['target_r_multiple']

        return {
            'timestamp': time.time(),
            'type': 'LONG',
            'instrument': 'US500',
            'entry': price,
            'stop': round(stop_price, 2),
            'target': round(target_price, 2),
            'confidence': round(confidence, 2),
            'sweep_impact': round(impact, 2),
            'risk_percent': round(stop_distance * 100, 2)
        }
