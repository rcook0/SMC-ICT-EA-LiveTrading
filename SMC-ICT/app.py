import time
import pandas as pd
import yfinance as yf
import streamlit as st
from smc_ict.strategy import build_signals

st.set_page_config(page_title="SMC/ICT Live", layout="wide")
st.title("SMC/ICT – Live Chart & Signals (M5)")

symbol = st.sidebar.text_input("Symbol (Yahoo format)", "BTC-USD")
refresh = st.sidebar.number_input("Refresh seconds", 15, 3600, 30)
lookback = st.sidebar.number_input("Lookback days", 1, 90, 7)

placeholder = st.empty()

def fetch(symbol, lookback):
    df = yf.download(symbol, period=f"{lookback}d", interval="5m", auto_adjust=True, threads=True)
    df = df.rename(columns=str.title)[['Open','High','Low','Close','Volume']].dropna()
    return df

while True:
    df = fetch(symbol, lookback)
    sig = build_signals(df)
    last = sig.iloc[-1]

    col1, col2 = st.columns([3,1])
    with col1:
        st.subheader(f"{symbol} – M5")
        st.line_chart(df['Close'], height=420)
    with col2:
        st.metric("Trend (H1)", "UP" if last['trend']==1 else "DOWN" if last['trend']==-1 else "NEUTRAL")
        st.metric("Long Signal", "YES" if last['long_sig'] else "NO")
        st.metric("Short Signal", "YES" if last['short_sig'] else "NO")
        st.write("SL/TP (derived from zones)")
        st.write({"sl_long": float(last['sl_long']), "tp_long": float(last['tp_long']),
                  "sl_short": float(last['sl_short']), "tp_short": float(last['tp_short'])})

    st.caption("Signals recompute every refresh interval. Backtester available via `python -m smc_ict.backtester`.")
    time.sleep(refresh)