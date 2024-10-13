import os
from datetime import datetime
from datetime import timedelta

from BackEnd.database.database import get_connection

# Import the calculateMovingAverage and calculateRSI functions from utils
from ..utils.moving_average_utils import calculateMovingAverage
from ..utils.rsi_utils import calculateRSI
from alpaca.data.requests import CryptoBarsRequest
from alpaca.data.timeframe import TimeFrame
from alpaca.data.historical import CryptoHistoricalDataClient
from dotenv import load_dotenv
from BackEnd.utils.reddit_data_analysis import reddit_data_analysis

load_dotenv()
api_key = os.getenv("ALPACA_API_KEY")
api_secret = os.getenv("ALPACA_SECRET")

# Fetch crypto data asynchronously
def get_crypto_data(target_day, period=21):

    client = CryptoHistoricalDataClient(api_key, api_secret)

    end_date = datetime.strptime(target_day, "%Y-%m-%d")
    start_date = end_date - timedelta(days=period + 1)

    request_params = CryptoBarsRequest(
        symbol_or_symbols=["BTC/USD"],
        timeframe=TimeFrame.Day,
        start=start_date,
        end=end_date
    )

    # Fetch historical crypto data
    try:
        bars = client.get_crypto_bars(request_params)
        return bars.df
    except Exception as e:
        raise Exception(f"Failed to fetch crypto data: {e}")


#goal is to get data and place it into the database on daily occurances

def daily_data_collection():
    # Call both the SMA and RSI functions
    print(f"Starting daily data collection on {datetime.now()}")

    reddit_data_analysis()

    # Fetch the data once
    target_day = datetime.today().strftime("%Y-%m-%d")
    crypto_data = get_crypto_data(target_day)
    last_row_close = crypto_data[['close']].tail(1)
    close = float(last_row_close['close'].values[0])

    # Calculate the Simple Moving Averages (SMA)
    sma_7, sma_21 = calculateMovingAverage(crypto_data)
    print(f"SMA 7: {sma_7}, SMA 21: {sma_21}")

    # Calculate the RSI
    rsi_value = calculateRSI(crypto_data)
    print(f"RSI: {rsi_value}")

    conn = get_connection()
    cursor = conn.cursor()
    try:
        query = """
        INSERT INTO daily_technical_analysis (date, closing_price, sma_7, sma_21, rsi)
        VALUES (%s, %s, %s, %s, %s)
        RETURNING *;
        """
        values = (target_day, close, sma_7, sma_21, rsi_value)
        cursor.execute(query, values)
        result = cursor.fetchone()
        print(result)
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise Exception(f"Failed to store sentiment score: {e}")
    finally:
        cursor.close()
        conn.close()

    print(f"Daily data collection completed on {datetime.now()}")



if __name__ == "__main__":
    daily_data_collection()