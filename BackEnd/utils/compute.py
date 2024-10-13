from alpaca.data.requests import CryptoBarsRequest
from alpaca.data.timeframe import TimeFrame
from alpaca.data.historical import CryptoHistoricalDataClient
from dotenv import load_dotenv
from datetime import datetime, timedelta
import os
from BackEnd.database.database import get_connection

# Load environment variables from .env file
load_dotenv()

# Use environment variables for Alpaca API credentials
api_key = os.getenv("ALPACA_API_KEY")
api_secret = os.getenv("ALPACA_SECRET")

client = CryptoHistoricalDataClient(api_key, api_secret)

def get_crypto_data(target_day, period=21):
    """
    Fetches the historical crypto data for the specified target day and period.
    """
    end_date = datetime.strptime(target_day, "%Y-%m-%d")
    start_date = end_date - timedelta(days=period + 1)  # Fetch enough data for both RSI and SMA

    # Create request object for historical crypto data
    request_params = CryptoBarsRequest(
        symbol_or_symbols=["BTC/USD"],  # Bitcoin symbol
        timeframe=TimeFrame.Day,  # Daily timeframe
        start=start_date,  # Start date for data retrieval
        end=end_date  # End date for data retrieval
    )

    # Fetch historical crypto data
    bars = client.get_crypto_bars(request_params)

    # Convert to DataFrame
    df = bars.df

    return df

def calculateMovingAverage(df):
    """
    Calculates the 7-day and 21-day moving averages using the given DataFrame.
    """
    # Calculate the 7-day and 21-day Simple Moving Averages (SMA)
    df['SMA_7'] = df['close'].rolling(window=7).mean()  # 7-day SMA
    df['SMA_21'] = df['close'].rolling(window=21).mean()  # 21-day SMA

    # Return the values of SMA_7 and SMA_21
    sma_7 = df.iloc[-1]['SMA_7']
    sma_21 = df.iloc[-1]['SMA_21']

    return sma_7, sma_21

def calculateRSI(df, period=14):
    """
    Calculates the RSI (Relative Strength Index) using the given DataFrame.
    """
    # Calculate the price differences between consecutive days
    df['diff'] = df['close'].diff(1)

    # Calculate gains and losses
    df['gain'] = df['diff'].apply(lambda x: x if x > 0 else 0)
    df['loss'] = df['diff'].apply(lambda x: -x if x < 0 else 0)

    # Calculate average gain and average loss over the period
    avg_gain = df['gain'].rolling(window=period, min_periods=1).mean()
    avg_loss = df['loss'].rolling(window=period, min_periods=1).mean()

    # Calculate RS (Relative Strength)
    rs = avg_gain / avg_loss

    # Calculate RSI
    df['RSI'] = 100 - (100 / (1 + rs))

    # Return the RSI value for the target day
    rsi_value = df.iloc[-1]['RSI']

    return rsi_value

# Fetch data once

def compute_all(date: datetime):
    date = date.strftime("%Y-%m-%d")
    crypto_data = get_crypto_data(date, period=21)

    # Calculate moving averages
    sma_7, sma_21 = calculateMovingAverage(crypto_data)

    #get close
    last_row_close = crypto_data[['close']].tail(1)
    close = float(last_row_close['close'].values[0])

    # Calculate RSI
    rsi = calculateRSI(crypto_data)
    
    conn = get_connection()
    cursor = conn.cursor()
    try:
        query = """
        INSERT INTO daily_technical_analysis (date, closing_price, sma_7, sma_21, rsi)
        VALUES (%s, %s, %s, %s, %s)
        RETURNING *;
        """
        values = (date, close, sma_7, sma_21, rsi)
        cursor.execute(query, values)
        result = cursor.fetchone()
        print(result)
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise Exception(f"Failed to store technical data: {e}")
    finally:
        cursor.close()
        conn.close()

    return {"rsi": rsi, "close": close, "sma_7": sma_7, "sma_21": sma_21}

def compute_all_wo_insert(date: datetime):
    date = date.strftime("%Y-%m-%d")
    crypto_data = get_crypto_data(date, period=21)

    # Calculate moving averages
    sma_7, sma_21 = calculateMovingAverage(crypto_data)

    #get close
    last_row_close = crypto_data[['close']].tail(1)
    close = float(last_row_close['close'].values[0])

    # Calculate RSI
    rsi = calculateRSI(crypto_data)


    return {"rsi": rsi, "close": close, "sma_7": sma_7, "sma_21": sma_21, "closing_price": close}
