import pandas as pd

def calculateRSI(df, period=14):
    """
    Calculates the RSI (Relative Strength Index) using the given DataFrame.
    """
    df['diff'] = df['close'].diff(1)

    df['gain'] = df['diff'].apply(lambda x: x if x > 0 else 0)
    df['loss'] = df['diff'].apply(lambda x: -x if x < 0 else 0)

    avg_gain = df['gain'].rolling(window=period, min_periods=1).mean()
    avg_loss = df['loss'].rolling(window=period, min_periods=1).mean()

    rs = avg_gain / avg_loss
    df['RSI'] = 100 - (100 / (1 + rs))

    rsi_value = df.iloc[-1]['RSI']

    return rsi_value
