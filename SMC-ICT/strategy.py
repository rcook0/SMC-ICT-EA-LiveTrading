import pandas as pd
from .indicators import trend_h1, fvg, order_block, breaker, sweeps

def resample(df, rule):
    agg = {'Open':'first','High':'max','Low':'min','Close':'last','Volume':'sum'}
    return df.resample(rule).agg(agg).dropna(how='any')

def build_signals(df_m5: pd.DataFrame) -> pd.DataFrame:
    # Derive M15 and H1 from M5
    df_m15 = resample(df_m5, '15T')
    df_h1  = resample(df_m5, '1H')

    tr = trend_h1(df_h1)
    tr_15 = tr.reindex(df_m15.index, method='ffill')

    f = fvg(df_m15)
    ob = order_block(df_m15, tr_15)
    br = breaker(df_m15, tr_15)
    sw = sweeps(df_m5)

    # Align to M5 for entries
    f5  = f.reindex(df_m5.index, method='ffill')
    ob5 = ob.reindex(df_m5.index, method='ffill')
    br5 = br.reindex(df_m5.index, method='ffill')
    tr5 = tr.reindex(df_m5.index, method='ffill')

    # Zone touches
    in_ob_long  = (tr5==1)  & (df_m5['Low']  <= ob5['ob_high'])
    in_ob_short = (tr5==-1) & (df_m5['High'] >= ob5['ob_low_s'])

    in_fvg_long  = (tr5==1)  & (df_m5['Low']  <= f5['fvg_high'])
    in_fvg_short = (tr5==-1) & (df_m5['High'] >= f5['fvg_low_bear'])

    in_br_long  = (tr5==1)  & (df_m5['Low']  <= br5['br_high'])
    in_br_short = (tr5==-1) & (df_m5['High'] >= br5['br_low_s'])

    micro_bull = df_m5['Close'] > df_m5['Open']
    micro_bear = df_m5['Close'] < df_m5['Open']

    long_sig  = (in_ob_long | in_fvg_long | in_br_long | sw['sweep_dn']) & micro_bull
    short_sig = (in_ob_short| in_fvg_short| in_br_short| sw['sweep_up'])  & micro_bear

    # SL/TP from zones (prefer FVG else OB else Breaker)
    sl_long = ob5['ob_low'].fillna(br5['br_low']).fillna(df_m5['Low'])
    tp_long = f5['fvg_high'].fillna(ob5['ob_high']).fillna(df_m5['Close']*1.01)

    sl_short= ob5['ob_high_s'].fillna(br5['br_high_s']).fillna(df_m5['High'])
    tp_short= f5['fvg_low_bear'].fillna(ob5['ob_low_s']).fillna(df_m5['Close']*0.99)

    out = pd.DataFrame({
        'trend':tr5, 'long_sig':long_sig, 'short_sig':short_sig,
        'sl_long':sl_long, 'tp_long':tp_long,
        'sl_short':sl_short,'tp_short':tp_short
    }, index=df_m5.index)
    return out