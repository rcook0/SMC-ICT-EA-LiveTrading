import pandas as pd
import numpy as np
import yfinance as yf
from .strategy import build_signals

def backtest(symbol="BTC-USD", interval="5m", lookback_days=30, risk_per_trade=0.01, fee_bp=5):
    df = yf.download(symbol, period=f"{lookback_days}d", interval=interval, auto_adjust=True, threads=True)
    df = df.rename(columns=str.title)[['Open','High','Low','Close','Volume']]
    df = df.dropna()
    sig = build_signals(df)

    balance = 10000.0
    equity = []
    pos = 0  # +1 long, -1 short
    entry = sl = tp = np.nan

    for t, row in sig.iterrows():
        price = df.loc[t, 'Close']
        # manage open position
        if pos != 0:
            if pos==1:
                if df.loc[t,'Low'] <= sl or df.loc[t,'High'] >= tp:
                    pnl = (tp if df.loc[t,'High']>=tp else sl) - entry
                    pnl -= price * (fee_bp/10000.0)
                    balance += pnl
                    pos=0
            else:
                if df.loc[t,'High'] >= sl or df.loc[t,'Low'] <= tp:
                    exit_price = (tp if df.loc[t,'Low']<=tp else sl)
                    pnl = entry - exit_price
                    pnl -= price * (fee_bp/10000.0)
                    balance += pnl
                    pos=0

        # open new trade
        if pos==0:
            risk_cash = balance * risk_per_trade
            if row['long_sig']:
                pos = 1
                entry = price
                sl = row['sl_long']
                tp = row['tp_long']
            elif row['short_sig']:
                pos = -1
                entry = price
                sl = row['sl_short']
                tp = row['tp_short']

        equity.append(balance if pos==0 else balance)  # simple equity curve

    res = {
        "trades_est": int((sig['long_sig']|sig['short_sig']).sum()),
        "final_balance": balance,
        "return_pct": (balance/10000.0 - 1.0)*100.0
    }
    eq = pd.Series(equity, index=sig.index, name="equity")
    return res, df, sig, eq

if __name__ == "__main__":
    res, df, sig, eq = backtest()
    print(res)