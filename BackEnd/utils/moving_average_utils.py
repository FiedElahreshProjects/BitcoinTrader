import pandas as pd

def calculateMovingAverage(df):
    """
    Calculates the 7-day and 21-day moving averages using the given DataFrame.
    """
    df['SMA_7'] = df['close'].rolling(window=7).mean()
    df['SMA_21'] = df['close'].rolling(window=21).mean()

    sma_7 = df.iloc[-1]['SMA_7']
    sma_21 = df.iloc[-1]['SMA_21']

    return sma_7, sma_21
