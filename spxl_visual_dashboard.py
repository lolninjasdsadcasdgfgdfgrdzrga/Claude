#!/usr/bin/env python3
"""
SPXL Volatility Analyzer - Interactive Visual Dashboard
Bloomberg Terminal Style with Charts and Graphs
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import yfinance as yf
from spxl_volatility_analyzer import SPXLAnalyzer
from datetime import datetime, timedelta

st.set_page_config(page_title="SPXL Volatility Analyzer", layout="wide", initial_sidebar_state="expanded")

# Custom CSS for Bloomberg Terminal style
st.markdown("""
    <style>
    .main {
        background-color: #0a0a0a;
        color: #fff;
    }
    .metric-card {
        background-color: #1a1a1a;
        padding: 20px;
        border-radius: 5px;
        border-left: 3px solid #00d4ff;
    }
    .signal-card {
        background-color: #1a1a1a;
        padding: 15px;
        border-radius: 5px;
        border-left: 3px solid #00ff00;
        margin-bottom: 10px;
    }
    </style>
""", unsafe_allow_html=True)

st.title("📈 SPXL Volatility Analyzer")
st.markdown("**Bloomberg Terminal Style - Real-Time Trading Signals**")
st.divider()

# Sidebar Configuration
with st.sidebar:
    st.header("⚙️ Configuration")

    data_source = st.radio("Data Source:", ["Live (yfinance)", "Sample Data", "Upload CSV"])

    if data_source == "Live (yfinance)":
        period = st.select_slider("Historical Data:", options=["1mo", "3mo", "6mo", "1y"], value="6mo")
        interval = st.selectbox("Timeframe:", ["1h", "4h", "1d"], index=0)

    account_size = st.number_input("Account Size ($):", value=10000, min_value=1000, step=1000)

    st.divider()
    st.markdown("**Risk Management**")
    risk_pct = st.slider("Risk per Trade (%):", 0.5, 5.0, 2.0, 0.5)
    max_positions = st.slider("Max Concurrent Positions:", 1, 5, 2)

# Load Data
try:
    if data_source == "Live (yfinance)":
        with st.spinner("📊 Downloading SPXL data..."):
            spxl = yf.download('SPXL', period=period, interval=interval, progress=False)
            df = pd.DataFrame({
                'timestamp': spxl.index,
                'open': spxl['Open'].values,
                'high': spxl['High'].values,
                'low': spxl['Low'].values,
                'close': spxl['Close'].values,
                'volume': spxl['Volume'].values
            })
    elif data_source == "Sample Data":
        with st.spinner("📊 Generating sample data..."):
            from spxl_terminal_dashboard import create_sample_data
            df = create_sample_data(days=30)
    else:  # Upload CSV
        uploaded_file = st.file_uploader("Choose CSV file", type="csv")
        if uploaded_file:
            df = pd.read_csv(uploaded_file)
        else:
            st.warning("Please upload a CSV file")
            st.stop()

    # Analyze
    with st.spinner("🔍 Analyzing patterns..."):
        analyzer = SPXLAnalyzer(df)
        report = analyzer.generate_comprehensive_report()

    # === HEADER METRICS ===
    st.markdown("### 📊 Market Metrics")
    col1, col2, col3, col4, col5, col6 = st.columns(6)

    with col1:
        st.metric("Price", f"${report['current_price']:.2f}", f"{report['change_pct']:.2f}%")
    with col2:
        st.metric("ATR (14)", f"${report['atr']:.2f}")
    with col3:
        st.metric("RSI (14)", f"{report['rsi']:.1f}")
    with col4:
        st.metric("Volatility (2D)", f"{report['volatility_2d']:.2f}%")
    with col5:
        color = "🔴" if report['regime'] == "HIGH_VOL" else "🟡" if report['regime'] == "NORMAL_VOL" else "🟢"
        st.metric("Regime", f"{color} {report['regime'].replace('_', ' ')}")
    with col6:
        st.metric("Volume Ratio", f"{report['volume_ratio']:.2f}x")

    st.divider()

    # === CANDLESTICK CHART WITH INDICATORS ===
    st.markdown("### 📈 Price Chart with Indicators")

    # Create subplots
    fig = make_subplots(
        rows=3, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.08,
        row_heights=[0.5, 0.25, 0.25],
        subplot_titles=("SPXL Price & Bollinger Bands", "RSI (14)", "MACD")
    )

    # Candlestick
    fig.add_trace(
        go.Candlestick(
            x=analyzer.data['timestamp'],
            open=analyzer.data['open'],
            high=analyzer.data['high'],
            low=analyzer.data['low'],
            close=analyzer.data['close'],
            name="SPXL",
            increasing_line_color='#00ff00',
            decreasing_line_color='#ff0000'
        ),
        row=1, col=1
    )

    # Bollinger Bands
    fig.add_trace(
        go.Scatter(
            x=analyzer.data['timestamp'],
            y=analyzer.data['bb_upper'],
            name="BB Upper",
            line=dict(color='#00d4ff', width=1, dash='dot'),
            hoverinfo='skip'
        ),
        row=1, col=1
    )

    fig.add_trace(
        go.Scatter(
            x=analyzer.data['timestamp'],
            y=analyzer.data['bb_lower'],
            name="BB Lower",
            line=dict(color='#00d4ff', width=1, dash='dot'),
            fill='tonexty',
            fillcolor='rgba(0, 212, 255, 0.1)',
            hoverinfo='skip'
        ),
        row=1, col=1
    )

    fig.add_trace(
        go.Scatter(
            x=analyzer.data['timestamp'],
            y=analyzer.data['sma_20'],
            name="SMA (20)",
            line=dict(color='#ffff00', width=1)
        ),
        row=1, col=1
    )

    # RSI
    fig.add_trace(
        go.Scatter(
            x=analyzer.data['timestamp'],
            y=analyzer.data['rsi'],
            name="RSI",
            line=dict(color='#ff9900', width=2)
        ),
        row=2, col=1
    )

    fig.add_hline(y=70, line_dash="dash", line_color="red", row=2, col=1)
    fig.add_hline(y=30, line_dash="dash", line_color="green", row=2, col=1)

    # MACD
    fig.add_trace(
        go.Scatter(
            x=analyzer.data['timestamp'],
            y=analyzer.data['macd'],
            name="MACD",
            line=dict(color='#00ff00', width=2)
        ),
        row=3, col=1
    )

    fig.add_trace(
        go.Scatter(
            x=analyzer.data['timestamp'],
            y=analyzer.data['macd_signal'],
            name="Signal",
            line=dict(color='#ff0000', width=2)
        ),
        row=3, col=1
    )

    # Update layout
    fig.update_layout(
        template="plotly_dark",
        hovermode="x unified",
        height=900,
        margin=dict(l=50, r=50, t=50, b=50),
        showlegend=True
    )

    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='#333333')
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#333333')

    st.plotly_chart(fig, use_container_width=True)

    st.divider()

    # === TRADING SIGNALS ===
    st.markdown("### 🎯 Trading Signals")

    if report['top_signals']:
        for idx, signal in enumerate(report['top_signals'][:5], 1):
            col1, col2, col3 = st.columns([2, 1, 2])

            with col1:
                score_color = "🟢" if signal['score'] >= 8.0 else "🟡" if signal['score'] >= 7.5 else "🔴"
                st.markdown(f"""
                **{score_color} [{idx}] {signal['pattern']}**

                *{signal['description']}*
                """)

            with col2:
                st.metric("Score", f"{signal['score']:.1f}/10")

            with col3:
                if signal.get('direction'):
                    st.metric("Direction", signal['direction'])
                    st.metric("Price", f"${signal['price']:.2f}")
                    if 'target' in signal:
                        st.metric("Target", f"${signal['target']:.2f}")
    else:
        st.info("No high-confidence patterns detected in current period.")

    st.divider()

    # === POSITION RECOMMENDATIONS ===
    st.markdown("### 💰 Position Recommendations")

    positions = []
    for signal in report['top_signals'][:3]:
        if signal.get('pattern') in ['OVERSOLD_REVERSAL', 'BULLISH_BREAKOUT']:
            atr = report['atr']
            current_price = report['current_price']
            stop_loss = signal.get('stop', current_price - atr * 1.5)
            risk_per_share = abs(current_price - stop_loss)
            risk_amount = account_size * (risk_pct / 100)
            shares = int(risk_amount / risk_per_share) if risk_per_share > 0 else 0

            if shares > 0:
                positions.append({
                    'Pattern': signal['pattern'],
                    'Direction': signal.get('direction', 'N/A'),
                    'Entry': f"${current_price:.2f}",
                    'Stop': f"${stop_loss:.2f}",
                    'Target': f"${signal.get('target', current_price + atr * 2):.2f}",
                    'Shares': shares,
                    'Position Value': f"${shares * current_price:,.0f}",
                    'Risk': f"${risk_amount:.0f}",
                    'Score': signal['score']
                })

    if positions:
        positions_df = pd.DataFrame(positions)
        st.dataframe(positions_df, use_container_width=True)

        # Summary
        col1, col2, col3 = st.columns(3)
        total_shares = sum([int(p['Shares']) for p in positions])
        total_value = sum([float(p['Position Value'].replace('$', '').replace(',', '')) for p in positions])
        total_risk = len(positions) * (account_size * risk_pct / 100)

        with col1:
            st.metric("Total Shares", total_shares)
        with col2:
            st.metric("Total Value", f"${total_value:,.0f}")
        with col3:
            st.metric("Total Risk", f"${total_risk:,.0f}")
    else:
        st.warning("No actionable positions at this time.")

    st.divider()

    # === MARKET INTERPRETATION ===
    st.markdown("### 📋 Market Interpretation")

    col1, col2, col3 = st.columns(3)

    with col1:
        if report['regime'] == 'LOW_VOL':
            vol_text = "SQUEEZED - Expect volatility expansion"
        elif report['regime'] == 'HIGH_VOL':
            vol_text = "ELEVATED - Take profits early"
        else:
            vol_text = "NORMAL - Standard conditions"
        st.info(f"**Volatility:** {vol_text}")

    with col2:
        if report['rsi'] < 30:
            rsi_text = "OVERSOLD - Potential bounce"
        elif report['rsi'] > 70:
            rsi_text = "OVERBOUGHT - Consider taking profits"
        else:
            rsi_text = "NEUTRAL - No extreme condition"
        st.info(f"**RSI Signal:** {rsi_text}")

    with col3:
        if report['bb_position'] < 20:
            bb_text = "Near Lower Band - Support"
        elif report['bb_position'] > 80:
            bb_text = "Near Upper Band - Resistance"
        else:
            bb_text = "Mid-range - Normal"
        st.info(f"**BB Position:** {bb_text}")

    st.markdown(f"""
    **Next 2 Days Forecast:**
    - Look for {report['regime'].split('_')[0]}-volatility moves around ${report['current_price']:.2f}
    - Max 2% account risk per position
    - Recommended hold time: 1-2 days
    - Exit on target, stop loss, or 2 ATR below entry
    """)

except Exception as e:
    st.error(f"Error: {str(e)}")
    st.info("Make sure your data has columns: timestamp, open, high, low, close, volume")
