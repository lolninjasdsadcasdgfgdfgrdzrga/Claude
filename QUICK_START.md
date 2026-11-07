# SPXL Volatility Analyzer - Quick Start Guide

## 🎯 What This Does

**Detects 1-2 day volatility trading patterns** in SPXL with Bloomberg Terminal-style analysis:
- ✅ Volatility squeezes (before big moves)
- ✅ Reversal signals (RSI + MACD confluence)
- ✅ Breakout setups (volume-confirmed)
- ✅ Position sizing (based on ATR & account risk)
- ✅ Entry/Exit levels with R:R calculations

---

## ⚡ 60-Second Setup

### Option A: Using Sample Data (Test Now)
```bash
cd /home/user/Claude
python3 spxl_terminal_dashboard.py
```
**Output**: Bloomberg Terminal display + position recommendations

### Option B: Using Your TradingView Data
1. **Export from TradingView**: 
   - Open SPXL, 1H or 4H timeframe
   - Right-click → Download data as CSV
   - Save as `spxl_data.csv`

2. **Run in Python**:
```python
from spxl_terminal_dashboard import load_tradingview_data, TerminalDashboard
from spxl_volatility_analyzer import SPXLAnalyzer

df = load_tradingview_data('spxl_data.csv')
analyzer = SPXLAnalyzer(df)
dashboard = TerminalDashboard(analyzer)
dashboard.print_full_dashboard(account_size=10000)  # Set your account size
```

### Option C: Live Data (yfinance)
```python
import yfinance as yf
import pandas as pd
from spxl_volatility_analyzer import SPXLAnalyzer

# Download 6 months of hourly data
spxl = yf.download('SPXL', period='6mo', interval='1h')

# Convert format
df = pd.DataFrame({
    'timestamp': spxl.index,
    'open': spxl['Open'],
    'high': spxl['High'],
    'low': spxl['Low'],
    'close': spxl['Close'],
    'volume': spxl['Volume']
})

# Analyze
analyzer = SPXLAnalyzer(df)
report = analyzer.generate_comprehensive_report()
```

---

## 📊 Understanding the Output

### Bloomberg Terminal Display Shows:

```
SPXL          PRICE: $88.63    CHG: +0.32%    REGIME: HIGH_VOL    ATR: 2.91    RSI: 41.2
───────────────────────────────────────────────────────────────────────────────────────

TOP TRADING SIGNALS (Ranked by Score):
[1] VOLATILITY_SQUEEZE | SCORE: 8.5/10 | Expected expansion coming
[2] BULLISH_BREAKOUT   | SCORE: 8.0/10 | Target: $102.85 | Stop: $91.30
[3] OVERSOLD_REVERSAL  | SCORE: 7.5/10 | Long entry at support
```

### Position Recommendations:

```
ENTRY: $88.63  |  STOP: $57.78  |  TARGET: $102.85  |  SHARES: 6  |  RISK:REWARD: 1.8x
```

### Key Metrics:

| Metric | What It Means | Action |
|--------|---------------|--------|
| **ATR** | Volatility measure | Higher = More movement expected |
| **RSI** | Overbought/Oversold | <30 = LONG, >70 = SHORT |
| **BB Width** | Squeeze level | Narrow = Breakout coming |
| **Volume Ratio** | Relative volume | >1.3x = Confirmation |
| **Regime** | Market condition | HIGH_VOL = Take profits early |

---

## 💰 Position Sizing Formula

```
Risk per Trade = Account Size × 2%
Stop Loss Distance = ATR × 1.5
Position Size = Risk ÷ Stop Distance

Example:
Account: $10,000
Risk: 2% = $200
ATR: $2.91
Stop: Entry - (2.91 × 1.5) = Entry - $4.37
Shares: $200 ÷ $4.37 = ~45 shares
```

---

## 📈 Trading Rules

### Entry Signals (Score ≥ 7.5):
- ✅ VOLATILITY_SQUEEZE + Volume expansion
- ✅ OVERSOLD_REVERSAL (RSI < 30 + MACD cross + volume)
- ✅ BULLISH_BREAKOUT (Close > BB Upper + 1.3x volume)

### Exit Rules:
- 📍 **Profit Target**: ATR × 2.5 from entry
- 🛑 **Stop Loss**: ATR × 1.5 below entry
- ⏰ **Time Stop**: 2-3 days maximum
- 💡 **Regime Stop**: If volatility drops, exit to preserve gains

### Risk Management:
- Max 2% per trade
- Max 2 concurrent positions
- Never average down
- Take 1/3 profits at 1:1 R:R

---

## 🔄 Daily Workflow

```
09:30 AM (Market Open + 15 min)
  ↓
  Run Analysis: python3 spxl_terminal_dashboard.py
  ↓
  Review Top Signals (Score ≥ 8.0)
  ↓
  Check Position Recommendations
  ↓
  Place Orders or SKIP if conditions weak
  ↓
11:00 AM - 2:00 PM
  ↓
  Monitor position, exit if target hit or stop touched
  ↓
3:00 PM (Last Hour)
  ↓
  Close any winning positions before close
  ↓
  Minimal holding overnight on SPXL
```

---

## 🎯 Pattern Recognition Guide

### Volatility Squeeze (Score: 8.5)
- Bollinger Bands at 20-period low
- Next candle ATR > current ATR
- Setup: Expect 3-5% move within 2 days
- Action: Wait for breakout direction

### Oversold Reversal (Score: 7.5)
- RSI < 30
- MACD histogram turns positive
- Volume > 20-period average
- Setup: Long entry at current price + support
- Target: RSI > 50

### Bullish Breakout (Score: 8.0)
- Close > Upper Bollinger Band
- Volume > 1.3x average
- MACD positive
- Setup: Continue long
- Target: Band width × 2 profit

---

## 📦 Files You Have

```
spxl_volatility_analyzer.py      # Core analysis engine
spxl_terminal_dashboard.py       # Bloomberg Terminal display
TRADINGVIEW_INTEGRATION.md       # How to integrate TradingView
GITHUB_TRADING_REPOS.md          # Best trading repos on GitHub
QUICK_START.md                   # This file
```

---

## 🚀 Next Steps

### For Testing (Today):
1. Run `python3 spxl_terminal_dashboard.py`
2. See sample analysis output
3. Understand pattern signals

### For Live Trading (This Week):
1. Export 3-6 months SPXL data from TradingView
2. Load into analyzer
3. Backtest on historical data
4. Paper trade on Alpaca first
5. Add Telegram alerts for real signals

### For Advanced (Next Week):
1. Integrate with Alpaca API
2. Set up daily automated runs
3. Create Telegram notifications
4. Track win rate & Sharpe ratio
5. Optimize parameters

---

## ⚠️ Important Disclaimers

- ⚡ **SPXL is 3x leveraged** - Volatility is amplified
- 💰 **2% risk = ~6-7% account drawdown** in worst case
- 📊 **Backtest before live trading**
- 🛑 **Use strict stops** - No exceptions
- 👨‍💻 **Monitor positions** - Don't set and forget

---

## 📞 Troubleshooting

**Q: Missing column error?**
```
A: Ensure CSV has: timestamp, open, high, low, close, volume
```

**Q: No patterns detected?**
```
A: Need at least 30 candles of data. Current: need 6 months history.
```

**Q: Stop loss too wide?**
```
A: Normal for volatile markets. Use ATR scaling. Reduce position size.
```

**Q: Want more indicators?**
```
A: Install pandas-ta: pip install pandas-ta
   Then add: df.ta.stoch(append=True) etc.
```

---

## 💡 Pro Tips

1. **Run analysis at 9:45 AM ET** - Wait 15 min after open for data stability
2. **Use 1H or 4H candles** - Best for 1-2 day trades (avoid 5m noise)
3. **Check regime first** - If HIGH_VOL, tighten stops and take profits early
4. **Volume is king** - Ignore signals without volume confirmation
5. **Track your trades** - Win rate + Sharpe ratio matter more than win size

---

**Ready? Start with `python3 spxl_terminal_dashboard.py` → see the output → then read integration guide!**
