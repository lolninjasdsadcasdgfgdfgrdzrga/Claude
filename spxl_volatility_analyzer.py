#!/usr/bin/env python3
"""
SPXL Volatility Pattern Analyzer - Bloomberg Terminal Style
Analyzes short-term (1-2 day) volatility patterns for swing trading
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Tuple
import warnings
warnings.filterwarnings('ignore')

class SPXLAnalyzer:
    def __init__(self, data: pd.DataFrame):
        """
        Initialize with OHLCV data
        Expected columns: ['timestamp', 'open', 'high', 'low', 'close', 'volume']
        """
        self.data = data.copy()
        self.data['timestamp'] = pd.to_datetime(self.data['timestamp'])
        self.data = self.data.sort_values('timestamp').reset_index(drop=True)
        self.calculate_indicators()

    def calculate_indicators(self):
        """Calculate technical indicators"""
        # ATR (Volatility measure)
        self.data['tr'] = np.maximum(
            self.data['high'] - self.data['low'],
            np.maximum(
                abs(self.data['high'] - self.data['close'].shift()),
                abs(self.data['low'] - self.data['close'].shift())
            )
        )
        self.data['atr_14'] = self.data['tr'].rolling(14).mean()

        # Bollinger Bands (20-period)
        self.data['sma_20'] = self.data['close'].rolling(20).mean()
        self.data['std_20'] = self.data['close'].rolling(20).std()
        self.data['bb_upper'] = self.data['sma_20'] + (self.data['std_20'] * 2)
        self.data['bb_lower'] = self.data['sma_20'] - (self.data['std_20'] * 2)
        self.data['bb_width'] = self.data['bb_upper'] - self.data['bb_lower']

        # RSI
        delta = self.data['close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
        rs = gain / loss
        self.data['rsi'] = 100 - (100 / (1 + rs))

        # MACD
        exp1 = self.data['close'].ewm(span=12).mean()
        exp2 = self.data['close'].ewm(span=26).mean()
        self.data['macd'] = exp1 - exp2
        self.data['macd_signal'] = self.data['macd'].ewm(span=9).mean()
        self.data['macd_hist'] = self.data['macd'] - self.data['macd_signal']

        # Volume analysis
        self.data['volume_sma'] = self.data['volume'].rolling(20).mean()
        self.data['volume_ratio'] = self.data['volume'] / self.data['volume_sma']

        # Price momentum
        self.data['returns'] = self.data['close'].pct_change() * 100
        self.data['volatility_2d'] = self.data['returns'].rolling(2).std()

    def detect_volatility_squeeze(self, lookback: int = 20) -> List[Dict]:
        """Detect Bollinger Band squeeze (low volatility before expansion)"""
        squeezes = []

        for i in range(lookback, len(self.data) - 1):
            current_width = self.data.iloc[i]['bb_width']
            past_width = self.data.iloc[i-lookback:i]['bb_width']
            percentile = (current_width < past_width.quantile(0.2))

            if percentile:
                next_atr = self.data.iloc[i+1]['atr_14']
                curr_atr = self.data.iloc[i]['atr_14']

                if next_atr and curr_atr and next_atr > curr_atr * 1.1:
                    squeezes.append({
                        'date': self.data.iloc[i]['timestamp'],
                        'score': 8.5,
                        'pattern': 'VOLATILITY_SQUEEZE',
                        'description': 'BB Squeeze with expected expansion',
                        'price': self.data.iloc[i]['close'],
                        'atr': curr_atr,
                        'bb_width': current_width
                    })

        return squeezes

    def detect_reversal_signals(self) -> List[Dict]:
        """Detect potential reversal points"""
        signals = []

        for i in range(2, len(self.data) - 1):
            rsi = self.data.iloc[i]['rsi']
            macd_hist = self.data.iloc[i]['macd_hist']
            prev_macd_hist = self.data.iloc[i-1]['macd_hist']
            close = self.data.iloc[i]['close']
            volume_ratio = self.data.iloc[i]['volume_ratio']

            # Oversold reversal (RSI < 30 + MACD crossover + volume)
            if rsi < 30 and prev_macd_hist < 0 and macd_hist > 0 and volume_ratio > 1.2:
                signals.append({
                    'date': self.data.iloc[i]['timestamp'],
                    'score': 7.5,
                    'pattern': 'OVERSOLD_REVERSAL',
                    'direction': 'LONG',
                    'description': 'Oversold + MACD Bullish Crossover + Volume',
                    'price': close,
                    'rsi': rsi,
                    'volume_ratio': volume_ratio
                })

            # Overbought reversal (RSI > 70 + MACD crossover + volume)
            elif rsi > 70 and prev_macd_hist > 0 and macd_hist < 0 and volume_ratio > 1.2:
                signals.append({
                    'date': self.data.iloc[i]['timestamp'],
                    'score': 7.5,
                    'pattern': 'OVERBOUGHT_REVERSAL',
                    'direction': 'SHORT',
                    'description': 'Overbought + MACD Bearish Crossover + Volume',
                    'price': close,
                    'rsi': rsi,
                    'volume_ratio': volume_ratio
                })

        return signals

    def detect_breakout_patterns(self) -> List[Dict]:
        """Detect breakout setups"""
        breakouts = []

        for i in range(5, len(self.data) - 1):
            close = self.data.iloc[i]['close']
            bb_upper = self.data.iloc[i]['bb_upper']
            bb_lower = self.data.iloc[i]['bb_lower']
            atr = self.data.iloc[i]['atr_14']
            volume_ratio = self.data.iloc[i]['volume_ratio']

            # Bullish breakout above upper BB
            if close > bb_upper and volume_ratio > 1.3:
                breakouts.append({
                    'date': self.data.iloc[i]['timestamp'],
                    'score': 8.0,
                    'pattern': 'BULLISH_BREAKOUT',
                    'direction': 'LONG',
                    'description': f'Break above BB Upper with {volume_ratio:.2f}x volume',
                    'price': close,
                    'target': close + (atr * 2),
                    'stop': close - (atr * 1.5)
                })

            # Bearish breakout below lower BB
            elif close < bb_lower and volume_ratio > 1.3:
                breakouts.append({
                    'date': self.data.iloc[i]['timestamp'],
                    'score': 8.0,
                    'pattern': 'BEARISH_BREAKOUT',
                    'direction': 'SHORT',
                    'description': f'Break below BB Lower with {volume_ratio:.2f}x volume',
                    'price': close,
                    'target': close - (atr * 2),
                    'stop': close + (atr * 1.5)
                })

        return breakouts

    def generate_comprehensive_report(self) -> Dict:
        """Generate full analysis report"""
        latest_idx = len(self.data) - 1
        latest = self.data.iloc[latest_idx]
        prev = self.data.iloc[latest_idx - 1]

        # Get all patterns
        squeezes = self.detect_volatility_squeeze()
        reversals = self.detect_reversal_signals()
        breakouts = self.detect_breakout_patterns()

        # Combine and sort by score
        all_signals = squeezes + reversals + breakouts
        all_signals.sort(key=lambda x: x.get('score', 0), reverse=True)

        # Market regime
        volatility = self.data['returns'].tail(5).std()
        if latest['atr_14']:
            atr_percentile = (latest['atr_14'] / self.data['atr_14'].max()) * 100
        else:
            atr_percentile = 50

        regime = 'HIGH_VOL' if atr_percentile > 75 else ('LOW_VOL' if atr_percentile < 25 else 'NORMAL_VOL')

        return {
            'timestamp': datetime.now(),
            'current_price': latest['close'],
            'prev_close': prev['close'],
            'change_pct': ((latest['close'] - prev['close']) / prev['close'] * 100),
            'regime': regime,
            'atr': latest['atr_14'],
            'rsi': latest['rsi'],
            'bb_position': (latest['close'] - latest['bb_lower']) / (latest['bb_upper'] - latest['bb_lower']) * 100 if latest['bb_width'] > 0 else 50,
            'volatility_2d': latest['volatility_2d'],
            'volume_ratio': latest['volume_ratio'],
            'top_signals': all_signals[:5],
            'total_patterns_detected': len(all_signals)
        }

def print_bloomberg_terminal(report: Dict):
    """Print report in Bloomberg Terminal style"""
    print("\n" + "="*120)
    print(f"{'SPXL VOLATILITY ANALYZER':^120}")
    print(f"{'Bloomberg Terminal Style - Short Term Trading Signals':^120}")
    print(f"{'Generated: ' + report['timestamp'].strftime('%Y-%m-%d %H:%M:%S UTC'):<120}")
    print("="*120)

    # Header Info
    print(f"\n {'SYMBOL':<15} {'PRICE':<15} {'CHG %':<12} {'REGIME':<15} {'ATR':<12} {'RSI':<10}")
    print("-"*120)
    print(f" {'SPXL':<15} {report['current_price']:<15.2f} {report['change_pct']:<12.2f} {report['regime']:<15} {report['atr']:<12.2f} {report['rsi']:<10.1f}")

    # Volatility Metrics
    print(f"\n {'VOLATILITY METRICS':<120}")
    print("-"*120)
    print(f" {'2D Volatility:':<30} {report['volatility_2d']:<15.2f}%")
    print(f" {'BB Position:':<30} {report['bb_position']:<15.1f}%")
    print(f" {'Volume Ratio:':<30} {report['volume_ratio']:<15.2f}x")

    # Signals
    print(f"\n {'TOP TRADING SIGNALS':<120}")
    print("-"*120)

    if report['top_signals']:
        for idx, signal in enumerate(report['top_signals'][:5], 1):
            print(f"\n [{idx}] {signal['pattern']:<30} SCORE: {signal['score']:<5.1f}/10")
            print(f"    Direction: {signal.get('direction', 'N/A'):<20} Price: ${signal['price']:<10.2f}")
            print(f"    {signal['description']}")
            if 'target' in signal:
                print(f"    Target: ${signal['target']:.2f} | Stop: ${signal['stop']:.2f}")
    else:
        print("\n No high-confidence patterns detected in current period.")

    print(f"\n {'SUMMARY':<120}")
    print("-"*120)
    print(f" Total Patterns Detected: {report['total_patterns_detected']:<10}")
    print(f" Recommendation: {'WATCH FOR SETUPS' if report['regime'] == 'LOW_VOL' else 'MONITOR FOR EXITS' if report['regime'] == 'HIGH_VOL' else 'NORMAL CONDITIONS'}")
    print("\n" + "="*120)


if __name__ == "__main__":
    print("SPXL Volatility Analyzer Ready")
    print("\nUsage:")
    print("1. Load OHLCV data from TradingView (Export as CSV)")
    print("2. Create analyzer: analyzer = SPXLAnalyzer(df)")
    print("3. Generate report: report = analyzer.generate_comprehensive_report()")
    print("4. Display: print_bloomberg_terminal(report)")
