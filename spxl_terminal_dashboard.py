#!/usr/bin/env python3
"""
SPXL Bloomberg Terminal Dashboard
Real-time volatility pattern analysis with position sizing
"""

import pandas as pd
import numpy as np
from spxl_volatility_analyzer import SPXLAnalyzer, print_bloomberg_terminal
from datetime import datetime, timedelta
from typing import Dict, List

class TerminalDashboard:
    """Bloomberg Terminal style dashboard with position recommendations"""

    def __init__(self, analyzer: SPXLAnalyzer):
        self.analyzer = analyzer
        self.report = analyzer.generate_comprehensive_report()

    def calculate_position_size(self, account_size: float, risk_pct: float = 2.0) -> Dict:
        """Calculate position size based on ATR and account risk"""
        atr = self.report['atr']
        current_price = self.report['current_price']

        # Risk per trade
        risk_amount = account_size * (risk_pct / 100)

        positions = []

        for signal in self.report['top_signals'][:3]:
            if signal.get('pattern') in ['OVERSOLD_REVERSAL', 'BULLISH_BREAKOUT']:
                stop_loss = signal.get('stop', current_price - atr * 1.5)
                risk_per_share = abs(current_price - stop_loss)
                shares = int(risk_amount / risk_per_share) if risk_per_share > 0 else 0
                position_value = shares * current_price

                positions.append({
                    'pattern': signal['pattern'],
                    'direction': signal.get('direction', 'LONG'),
                    'entry': current_price,
                    'stop': stop_loss,
                    'target': signal.get('target', current_price + atr * 2),
                    'shares': shares,
                    'position_value': position_value,
                    'risk': risk_amount,
                    'reward': position_value * (signal['score'] / 10) * 0.05,  # Estimated reward
                    'score': signal['score']
                })

        return positions

    def print_position_recommendations(self, account_size: float = 10000):
        """Print trading recommendations"""
        positions = self.calculate_position_size(account_size)

        print("\n" + "="*140)
        print(f"{'POSITION RECOMMENDATIONS':<140}")
        print(f"{'Account Size: ${:,.0f} | Risk per Trade: 2% (${:,.0f})':<140}".format(
            account_size, account_size * 0.02))
        print("="*140)

        if not positions:
            print("\nNo actionable positions at this time.")
            print("\nWaiting for better setups...")
            return

        print(f"\n{'RANK':<6} {'PATTERN':<25} {'DIRECTION':<12} {'ENTRY':<12} {'STOP':<12} {'TARGET':<12} {'SHARES':<10} {'RISK:REWARD':<15}")
        print("-"*140)

        for idx, pos in enumerate(positions, 1):
            risk_reward = pos['reward'] / pos['risk'] if pos['risk'] > 0 else 0
            direction_display = f"[{pos['direction']}]"

            print(f" {idx:<5} {pos['pattern']:<25} {direction_display:<12} "
                  f"${pos['entry']:<11.2f} ${pos['stop']:<11.2f} ${pos['target']:<11.2f} "
                  f"{pos['shares']:<10} {risk_reward:<15.2f}")

    def print_full_dashboard(self, account_size: float = 10000):
        """Print complete dashboard"""
        print_bloomberg_terminal(self.report)
        self.print_position_recommendations(account_size)
        print("\n" + "="*140)
        print(f"{'MARKET INTERPRETATION':<140}")
        print("="*140)
        self._print_market_interpretation()
        print("\n" + "="*140)

    def _print_market_interpretation(self):
        """Print human-readable market analysis"""
        report = self.report

        # Volatility interpretation
        if report['regime'] == 'LOW_VOL':
            vol_text = "SQUEEZED - Expect volatility expansion. Watch for breakout setups."
        elif report['regime'] == 'HIGH_VOL':
            vol_text = "ELEVATED - Take profits on winners, set tight stops."
        else:
            vol_text = "NORMAL - Standard trading conditions."

        # RSI interpretation
        if report['rsi'] < 30:
            rsi_text = "OVERSOLD - Potential bounce expected."
        elif report['rsi'] > 70:
            rsi_text = "OVERBOUGHT - Consider taking profits."
        else:
            rsi_text = "NEUTRAL - No extreme condition."

        # BB Position
        if report['bb_position'] < 20:
            bb_text = "Near Lower Band - Potential support."
        elif report['bb_position'] > 80:
            bb_text = "Near Upper Band - Potential resistance."
        else:
            bb_text = "Mid-range - Normal position."

        print(f"\n Volatility Regime: {vol_text}")
        print(f" RSI Signal:       {rsi_text}")
        print(f" BB Position:      {bb_text}")
        print(f"\n → Next 2 Days: Look for {report['regime'].split('_')[0]}-volatility moves around ${report['current_price']:.2f}")
        print(f" → Trade Size: Max 2% account risk per position (2 concurrent positions suggested)")
        print(f" → Timeframe: 1-2 day holds, exit on target or 2 ATR stop loss")


def load_tradingview_data(filepath: str) -> pd.DataFrame:
    """Load data exported from TradingView (expected format: Time, Open, High, Low, Close, Volume)"""
    df = pd.read_csv(filepath)
    df.columns = ['timestamp', 'open', 'high', 'low', 'close', 'volume']
    return df


# Example usage with sample data
def create_sample_data(days: int = 30) -> pd.DataFrame:
    """Generate realistic SPXL sample data for demonstration"""
    base_date = datetime.now() - timedelta(days=days)
    prices = []
    close = 50.0  # Starting price

    for i in range(days * 6):  # 6 periods per day (4-hour candles)
        timestamp = base_date + timedelta(hours=4*i)

        # Random walk with mean reversion
        change = np.random.normal(0.002, 0.02)  # SPXL is volatile
        close = close * (1 + change)
        open_p = close * (1 + np.random.normal(0, 0.01))
        high = max(open_p, close) * (1 + abs(np.random.normal(0, 0.01)))
        low = min(open_p, close) * (1 - abs(np.random.normal(0, 0.01)))
        volume = int(np.random.normal(2000000, 500000))

        prices.append({
            'timestamp': timestamp,
            'open': open_p,
            'high': high,
            'low': low,
            'close': close,
            'volume': max(volume, 500000)
        })

    return pd.DataFrame(prices)


if __name__ == "__main__":
    # Load sample data
    print("Generating sample SPXL data...")
    df = create_sample_data(days=30)

    # Create analyzer
    print("Analyzing patterns...")
    analyzer = SPXLAnalyzer(df)

    # Create dashboard
    dashboard = TerminalDashboard(analyzer)

    # Display full dashboard with $10,000 account
    print("\n\n")
    dashboard.print_full_dashboard(account_size=10000)

    print("\n\nTO USE WITH YOUR DATA:")
    print("1. Export SPXL 1H or 4H data from TradingView as CSV")
    print("2. Run: df = load_tradingview_data('your_file.csv')")
    print("3. Run: analyzer = SPXLAnalyzer(df)")
    print("4. Run: dashboard = TerminalDashboard(analyzer)")
    print("5. Run: dashboard.print_full_dashboard(account_size=YOUR_ACCOUNT_SIZE)")
