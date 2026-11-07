# SPXL Volatility Pattern Analyzer
## Bloomberg Terminal-Style Trading Machine for 1-2 Day Swings

A precision pattern recognition system for detecting short-term volatility trading opportunities in SPXL with professional-grade analysis and Bloomberg Terminal aesthetic.

---

## 🎯 What You Get

### Core Features
✅ **Volatility Squeeze Detection** - Identifies Bollinger Band compression before explosive moves  
✅ **Reversal Signals** - RSI + MACD confluence patterns for mean reversion trades  
✅ **Breakout Analysis** - Volume-confirmed breakouts with targets & stops  
✅ **Position Sizing** - ATR-based risk calculations (2% account risk)  
✅ **Bloomberg Terminal UI** - Professional formatted output with metrics dashboard  
✅ **Integration Ready** - TradingView CSV export, yfinance, Alpaca API support  

### Technical Indicators Included
- ATR (14-period) - Volatility measure for stop/target sizing
- Bollinger Bands (20-period) - Support/resistance & squeeze detection
- RSI (14-period) - Overbought/oversold conditions
- MACD - Momentum & trend confirmation
- Volume Analysis - Breakout confirmation & strength validation

---

## 📁 Files Included

### Code Files
| File | Purpose |
|------|---------|
| `spxl_volatility_analyzer.py` | Core analysis engine with pattern detection |
| `spxl_terminal_dashboard.py` | Bloomberg Terminal display & position sizing |

### Documentation
| File | Purpose |
|------|---------|
| `QUICK_START.md` | 60-second setup guide & trading rules |
| `TRADINGVIEW_INTEGRATION.md` | 4 methods to get data + live automation |
| `GITHUB_TRADING_REPOS.md` | Top 10 trading analysis libraries |
| `README.md` | This file |

---

## 🚀 Quick Start (Choose One)

### Option 1: Test with Sample Data (Right Now!)
```bash
python3 spxl_terminal_dashboard.py
```
Generates fake but realistic SPXL data and shows full analysis.

### Option 2: Use Your TradingView Data
```python
from spxl_terminal_dashboard import load_tradingview_data, TerminalDashboard
from spxl_volatility_analyzer import SPXLAnalyzer

df = load_tradingview_data('your_spxl_export.csv')
analyzer = SPXLAnalyzer(df)
dashboard = TerminalDashboard(analyzer)
dashboard.print_full_dashboard(account_size=10000)
```

### Option 3: Live Data with yfinance
```python
import yfinance as yf
from spxl_volatility_analyzer import SPXLAnalyzer

spxl = yf.download('SPXL', period='6mo', interval='1h')
analyzer = SPXLAnalyzer(spxl)
report = analyzer.generate_comprehensive_report()
```

---

## 📊 Output Example

```
════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
                                              SPXL VOLATILITY ANALYZER
                                Bloomberg Terminal Style - Short Term Trading Signals
Generated: 2026-11-07 09:44:40 UTC
════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════

 SYMBOL          PRICE           CHG %        REGIME          ATR          RSI       
────────────────────────────────────────────────────────────────────────────────────
 SPXL            88.63           0.32         HIGH_VOL        2.91         41.2      

 TOP TRADING SIGNALS
────────────────────────────────────────────────────────────────────────────────────

 [1] VOLATILITY_SQUEEZE             SCORE: 8.5  /10
    Description: BB Squeeze with expected expansion

 [2] BULLISH_BREAKOUT               SCORE: 8.0  /10
    Entry: $88.63  |  Stop: $57.78  |  Target: $102.85  |  Shares: 6

 [3] OVERSOLD_REVERSAL              SCORE: 7.5  /10
    Direction: LONG  |  Price: $88.63  |  Volume Ratio: 1.23x

════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
```

---

## 💰 How It Works

### 1. Pattern Detection (3 Types)

**Volatility Squeeze (Score: 8.5/10)**
- Bollinger Band width at 20-period low
- Next ATR expansion expected
- Setup: Prepare for 3-5% move within 2 days

**Oversold/Overbought Reversal (Score: 7.5/10)**
- RSI < 30 (oversold) or > 70 (overbought)
- MACD histogram crosses to opposite side
- Volume confirms
- Setup: Mean reversion trade

**Breakout (Score: 8.0/10)**
- Close breaks above/below Bollinger Bands
- Volume > 1.3x average
- MACD confirms direction
- Setup: Momentum continuation

### 2. Position Sizing
```
Risk per trade = Account size × 2% (e.g., $10K → $200 risk)
Stop loss = ATR × 1.5 below entry
Profit target = ATR × 2.5 above entry
Shares = Risk ÷ (Entry - Stop)
```

### 3. Market Regime
- **LOW_VOL**: Prepare for breakout setups
- **NORMAL_VOL**: Standard trading conditions
- **HIGH_VOL**: Take profits early, tighten stops

---

## 🎓 Key Metrics Explained

| Metric | Range | Interpretation |
|--------|-------|-----------------|
| **Signal Score** | 7.0-10.0 | Confidence level (7.5+ = trade) |
| **ATR** | Per security | Stop/target distance in dollars |
| **RSI** | 0-100 | <30 Long, 30-70 Neutral, >70 Short |
| **BB Width** | Low-High | Squeeze when at 20-period lows |
| **Volume Ratio** | 1.0x+ | Breakout needs >1.3x confirmation |
| **Regime** | 3 states | Sets stop/exit strategy |

---

## 🔄 Recommended Workflow

### Daily (9:45 AM ET)
1. Run analysis script
2. Review top 3 signals
3. Filter by: Score ≥ 7.5 + Volume ≥ 1.2x
4. Check current positions

### During Trading Hours
1. Monitor entries if signal triggers
2. Set stops at ATR × 1.5
3. Trail stops after 1:1 profit
4. Close by 3:00 PM (before close volatility)

### Post-Close
1. Track wins/losses
2. Review what worked
3. Update your rules

---

## 📈 What Makes This Different

1. **Precision Volatility Focus** - Not trend-following, but volatility-optimized for 1-2 day holds
2. **Bloomberg Terminal Aesthetic** - Professional output (not random indicators)
3. **Confluence-Based** - Signals require 2+ indicators to align (RSI + MACD + Volume)
4. **Risk-First** - All recommendations include ATR-based stops
5. **Production-Ready** - Integrates with real brokers (Alpaca) and data sources

---

## 🔗 Integration Paths

### Beginner: CSV Import (Week 1)
- Export from TradingView → Load into analyzer → Get signals manually

### Intermediate: Automated Daily (Week 2)
- yfinance pulls data daily → Analyzer runs automatically → Get email/Telegram alerts

### Advanced: Live Trading (Week 3)
- Real-time data → Alpaca API execution → Automated position management

See `TRADINGVIEW_INTEGRATION.md` for detailed setup for each level.

---

## 📚 External Resources

### Top Trading Libraries (from GitHub)
- **TA-Lib** (10k⭐) - 200+ technical indicators
- **pandas-ta** (4k⭐) - 150+ indicators with pandas
- **backtrader** (12k⭐) - Backtesting framework
- **vectorbt** (5k⭐) - Fast optimization
- **yfinance** (12k⭐) - Free market data

See `GITHUB_TRADING_REPOS.md` for 10 detailed recommendations.

---

## ⚙️ Requirements

```bash
pip install pandas numpy scikit-learn
```

**Optional (for enhancements):**
```bash
pip install pandas-ta        # More indicators
pip install yfinance         # Live data
pip install alpaca-trade-api # Live trading
```

---

## ⚠️ Risk Disclaimer

- **SPXL is 3x leveraged** - This multiplies both gains AND losses
- **2% risk rule** - Can still result in 6-7% account drawdown in worst case
- **No guarantees** - Past patterns don't guarantee future results
- **Monitor positions** - Don't set and forget
- **Paper trade first** - Test on Alpaca before real money
- **Use stops religiously** - No exceptions, no averaging down

---

## 🔧 Customization

Modify in `spxl_volatility_analyzer.py`:

```python
# Change ATR period
self.data['atr_14'] = ...  # → change to atr_21, atr_7, etc.

# Change Bollinger Bands period
self.data['bb_20'] = ...  # → change to bb_10, bb_30, etc.

# Change RSI threshold
if rsi < 30:  # → change to 25 or 35 for tighter/looser

# Adjust volatility percentile for squeeze
if percentile < 0.2:  # → change to 0.1 (tighter) or 0.3 (looser)
```

---

## 📞 Troubleshooting

**No patterns detected?**
- Need minimum 30 bars of data (6 months of hourly = 4,380 bars ✓)

**Stop loss too wide?**
- Normal for volatile markets; adjust position size down

**Want to add more indicators?**
```python
pip install pandas-ta
import pandas_ta as ta
df.ta.stoch(append=True)  # Add Stochastic
df.ta.adx(append=True)    # Add ADX for trend strength
```

**How to enable Telegram alerts?**
- See `TRADINGVIEW_INTEGRATION.md` → Section "Mobile Alerts"

---

## 📋 Checklist Before Live Trading

- [ ] Backtested on 3+ months of data
- [ ] Paper traded for 2 weeks (Alpaca)
- [ ] Win rate > 40% observed
- [ ] Largest loss < 2 × smallest win
- [ ] Account risk per trade = 2% max
- [ ] Stops are set BEFORE entry (not afterwards)
- [ ] You understand all parameters

---

## 🎯 Next Steps

1. **Today**: Run `python3 spxl_terminal_dashboard.py` → See sample output
2. **This Week**: Export real TradingView data → Load it → Analyze
3. **Next Week**: Set up yfinance automation → Daily runs
4. **Following Week**: Paper trade signals → Track results
5. **Month 2**: Real trading (after 4+ weeks observation)

---

## 💬 Questions?

Check files in order:
1. `QUICK_START.md` - Common questions answered
2. `TRADINGVIEW_INTEGRATION.md` - Data & automation questions
3. `GITHUB_TRADING_REPOS.md` - "Which library should I use?"

---

**Happy trading! Remember: *Precision beats speed, discipline beats emotion, and risk management beats everything.*** 📊

---

*Built with precision for 1-2 day SPXL volatility trading | Bloomberg Terminal style | Production-ready*
