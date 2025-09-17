import numpy as np
import pandas as pd

def swings(h, l, lookback=2):
    hh = (h.shift(1) > h.shift(2)) & (l.shift(1) > l.shift(2))
    ll = (h.shift(1) < h.shift(2)) & (l.shift(1) < l.shift(2))
    return hh.rename("trend_up"), ll.rename("trend_dn")

def trend_h1(df_h1: pd.DataFrame) -> pd.Series:
    up, dn = swings(df_h1['High'], df_h1['Low'])
    tr = pd.Series(0, index=df_h1.index)
    tr[up] = 1
    tr[dn] = -1
    return tr.replace(to_replace=0, method='ffill').fillna(0).rename("trend")

def fvg(df: pd.DataFrame) -> pd.DataFrame:
    h0, l0 = df['High'].shift(2), df['Low'].shift(2)
    h2, l2 = df['High'], df['Low']
    bull = (l0 > h2)
    bear = (h0 < l2)
    return pd.DataFrame({
        'fvg_low':  np.where(bull, h2, np.nan),
        'fvg_high': np.where(bull, l0, np.nan),
        'fvg_low_bear':  np.where(bear, h0, np.nan),
        'fvg_high_bear': np.where(bear, l2, np.nan),
    }, index=df.index)

def order_block(df: pd.DataFrame, trend: pd.Series) -> pd.DataFrame:
    # last opposite candle body range
    red  = df['Close'].shift(2) < df['Open'].shift(2)
    green= df['Close'].shift(2) > df['Open'].shift(2)
    ob_low  = np.where((trend==1) & red,  df['Low'].shift(2),  np.nan)
    ob_high = np.where((trend==1) & red,  df['High'].shift(2), np.nan)
    ob_low_s= np.where((trend==-1) & green, df['Low'].shift(2),  np.nan)
    ob_high_s= np.where((trend==-1) & green, df['High'].shift(2), np.nan)
    return pd.DataFrame({
        'ob_low':ob_low,'ob_high':ob_high,
        'ob_low_s':ob_low_s,'ob_high_s':ob_high_s
    }, index=df.index)

def breaker(df: pd.DataFrame, trend: pd.Series) -> pd.DataFrame:
    strong_up   = (df['Close'].shift(1) > df['Open'].shift(1)) & (df['Close'].shift(1) > df['High'].shift(2))
    strong_down = (df['Close'].shift(1) < df['Open'].shift(1)) & (df['Close'].shift(1) < df['Low'].shift(2))
    br_low  = np.where((trend==1) & strong_up,   df['Low'].shift(1),  np.nan)
    br_high = np.where((trend==1) & strong_up,   df['High'].shift(1), np.nan)
    br_low_s= np.where((trend==-1) & strong_down,df['Low'].shift(1),  np.nan)
    br_high_s=np.where((trend==-1)& strong_down, df['High'].shift(1), np.nan)
    return pd.DataFrame({
        'br_low':br_low,'br_high':br_high,
        'br_low_s':br_low_s,'br_high_s':br_high_s
    }, index=df.index)

def sweeps(df_m5: pd.DataFrame, window=10) -> pd.DataFrame:
    prev_h = df_m5['High'].rolling(window).max().shift(1)
    prev_l = df_m5['Low'].rolling(window).min().shift(1)
    up = df_m5['High'] > prev_h
    dn = df_m5['Low']  < prev_l
    return pd.DataFrame({'sweep_up':up, 'sweep_dn':dn}, index=df_m5.index)