# TradingView Integration Guide for SPXL Analyzer

## ✅ Method 1: CSV Export (Recommended - Simplest)

### Step 1: Export from TradingView
1. Open TradingView chart (SPXL, 1H or 4H timeframe)
2. Right-click on chart → "Download data"
3. Select format: CSV
4. Save as `spxl_data.csv`

### Step 2: Load into Analyzer
```python
from spxl_terminal_dashboard import load_tradingview_data, TerminalDashboard
from spxl_volatility_analyzer import SPXLAnalyzer

# Load the CSV you exported
df = load_tradingview_data('spxl_data.csv')

# Analyze
analyzer = SPXLAnalyzer(df)
dashboard = TerminalDashboard(analyzer)

# Display Bloomberg Terminal
dashboard.print_full_dashboard(account_size=10000)
```

---

## 🔔 Method 2: Webhook Alerts (Real-Time)

### Setup TradingView Alert with Webhook

**Create a Pine Script Alert Trigger:**

```pinescript
//@version=5
indicator("SPXL Alert", overlay=true)

// Bollinger Squeeze
bb_length = 20
bb_src = close
basis = ta.sma(bb_src, bb_length)
dev = ta.stdev(bb_src, bb_length)
upper_bb = basis + (dev * 2)
lower_bb = basis - (dev * 2)
bb_width = upper_bb - lower_bb

// Squeeze condition
is_squeeze = bb_width < ta.percentile_nearest(bb_width, 20, 20)

// Alert
alertcondition(is_squeeze, title="Volatility Squeeze", message="SPXL Squeeze Detected!")
```

**Configure Alert:**
1. Chart → Alert → Create Alert
2. Condition: "SPXL Alert Volatility Squeeze"
3. Webhook URL: `http://your-server.com/webhook`
4. Message: 
```json
{
  "symbol": "SPXL",
  "pattern": "{{strategy.order.comment}}",
  "price": "{{close}}",
  "time": "{{timenow}}"
}
```

---

## 💾 Method 3: Python + yfinance (Automated)

### Real-time Data with yfinance

```python
import yfinance as yf
import pandas as pd
from spxl_volatility_analyzer import SPXLAnalyzer
from spxl_terminal_dashboard import TerminalDashboard

def analyze_spxl_live():
    """Download SPXL data and analyze"""
    
    # Download 6 months of 1H data
    spxl = yf.download('SPXL', period='6mo', interval='1h')
    
    # Rename columns to match our analyzer
    spxl_clean = pd.DataFrame({
        'timestamp': spxl.index,
        'open': spxl['Open'].values,
        'high': spxl['High'].values,
        'low': spxl['Low'].values,
        'close': spxl['Close'].values,
        'volume': spxl['Volume'].values
    })
    
    # Analyze
    analyzer = SPXLAnalyzer(spxl_clean)
    dashboard = TerminalDashboard(analyzer)
    dashboard.print_full_dashboard(account_size=15000)
    
    return dashboard.report

# Run daily
if __name__ == "__main__":
    report = analyze_spxl_live()
    print(f"\n✓ Analysis Complete: {len(report['top_signals'])} patterns detected")
```

### Scheduling (Auto-run daily):

```bash
# Add to crontab (runs 9:30 AM daily)
30 9 * * MON-FRI python3 /path/to/spxl_live_analysis.py
```

---

## 🤖 Method 4: Alpaca Paper Trading (Test Your Signals)

### Setup Alpaca (Free paper trading account)

```python
from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce

# Initialize
api_key = "YOUR_ALPACA_API_KEY"
secret_key = "YOUR_ALPACA_SECRET_KEY"
client = TradingClient(api_key, secret_key, paper=True)

# Get account
account = client.get_account()
print(f"Account Balance: ${account.cash}")

# Get SPXL position
try:
    position = client.get_open_position("SPXL")
    print(f"Current Position: {position.qty} shares @ ${position.current_price}")
except:
    print("No SPXL position")

# Place order based on signal
def execute_signal(analyzer, signal):
    if signal['direction'] == 'LONG':
        order = MarketOrderRequest(
            symbol="SPXL",
            qty=signal.get('shares', 10),
            side=OrderSide.BUY,
            time_in_force=TimeInForce.DAY
        )
    else:  # SHORT
        order = MarketOrderRequest(
            symbol="SPXL",
            qty=signal.get('shares', 10),
            side=OrderSide.SELL,
            time_in_force=TimeInForce.DAY
        )
    
    order_data = client.submit_order(order)
    print(f"✓ Order Placed: {order_data}")

# Example usage
# execute_signal(analyzer, analyzer.report['top_signals'][0])
```

---

## 📊 Advanced: Add More Indicators

```python
import pandas_ta as ta
import yfinance as yf

# Get data
spxl = yf.download('SPXL', period='3mo', interval='1h')

# Add indicators
spxl.ta.atr(length=14, append=True)
spxl.ta.rsi(length=14, append=True)
spxl.ta.macd(append=True)
spxl.ta.bbands(length=20, append=True)
spxl.ta.stoch(append=True)  # Stochastic
spxl.ta.adx(length=14, append=True)  # Trend strength
spxl.ta.volume_profile(append=True)  # Volume levels

# Your analyzer gets all these
from spxl_volatility_analyzer import SPXLAnalyzer
analyzer = SPXLAnalyzer(spxl)
```

---

## ⚡ Complete Automated Workflow

```python
#!/usr/bin/env python3
"""Daily SPXL Analysis + Alpaca Paper Trading"""

import schedule
import time
import yfinance as yf
import pandas as pd
from datetime import datetime
from spxl_volatility_analyzer import SPXLAnalyzer
from spxl_terminal_dashboard import TerminalDashboard, TerminalDashboard
from alpaca.trading.client import TradingClient

class SPXLTradingBot:
    def __init__(self, account_size=10000):
        self.account_size = account_size
        self.client = TradingClient(
            api_key="YOUR_KEY",
            secret_key="YOUR_SECRET",
            paper=True
        )
    
    def analyze(self):
        """Download data and analyze"""
        spxl = yf.download('SPXL', period='3mo', interval='1h')
        spxl_clean = pd.DataFrame({
            'timestamp': spxl.index,
            'open': spxl['Open'].values,
            'high': spxl['High'].values,
            'low': spxl['Low'].values,
            'close': spxl['Close'].values,
            'volume': spxl['Volume'].values
        })
        
        analyzer = SPXLAnalyzer(spxl_clean)
        dashboard = TerminalDashboard(analyzer)
        return dashboard
    
    def daily_job(self):
        """Run daily analysis"""
        print(f"\n[{datetime.now()}] Running SPXL Analysis...")
        
        dashboard = self.analyze()
        dashboard.print_full_dashboard(self.account_size)
        
        # Save report
        with open('spxl_reports.txt', 'a') as f:
            f.write(f"\n{'='*100}\n")
            f.write(f"Report: {datetime.now()}\n")
            f.write(f"Top Signal: {dashboard.report['top_signals'][0] if dashboard.report['top_signals'] else 'None'}\n")
    
    def start(self):
        """Start scheduler"""
        schedule.every().day.at("09:30").do(self.daily_job)
        
        while True:
            schedule.run_pending()
            time.sleep(60)

if __name__ == "__main__":
    bot = SPXLTradingBot(account_size=15000)
    bot.daily_job()  # Run immediately
    # bot.start()  # Uncomment for continuous scheduling
```

---

## 🎯 Performance Tips

1. **Use 1H or 4H candles** (1D too slow, 5m too noisy)
2. **Keep last 90 days of data** (enough for 20-period MA)
3. **Run analysis 15 min after market open** (9:45 AM ET)
4. **Check exits before 3:00 PM ET** (last hour volatility)
5. **Use 2% account risk max per trade**
6. **Hold 1-2 days only** (your sweet spot)

---

## ⚠️ Risk Management Rules

```python
# From dashboard.report:
max_risk = account_size * 0.02  # 2% per trade
atr = dashboard.report['atr']
current_price = dashboard.report['current_price']

# Entry rules:
if score >= 7.5 and volume_ratio > 1.2:
    entry = current_price
    stop = entry - (atr * 1.5)
    target = entry + (atr * 2.5)
    shares = int(max_risk / abs(entry - stop))
```

---

## 📱 Mobile Alerts (Optional)

```python
import requests

def send_telegram_alert(message):
    """Send signal to Telegram"""
    token = "YOUR_BOT_TOKEN"
    chat_id = "YOUR_CHAT_ID"
    
    requests.post(
        f"https://api.telegram.org/bot{token}/sendMessage",
        data={"chat_id": chat_id, "text": message}
    )

# Use it
signal = dashboard.report['top_signals'][0]
message = f"🚀 SPXL Signal!\n{signal['pattern']}\nEntry: ${signal['price']}"
send_telegram_alert(message)
```

---

**Your setup is now complete. Start with Method 1, upgrade to Method 3 when you're ready.**
