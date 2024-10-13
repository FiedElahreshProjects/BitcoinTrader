import os
from datetime import datetime
import asyncio
import pandas as pd
import praw
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from datetime import datetime
from datetime import timedelta

# Import the calculateMovingAverage and calculateRSI functions from utils
from ..utils.moving_average_utils import calculateMovingAverage
from ..utils.rsi_utils import calculateRSI
from alpaca.data.requests import CryptoBarsRequest
from alpaca.data.timeframe import TimeFrame
from alpaca.data.historical import CryptoHistoricalDataClient
from dotenv import load_dotenv


# Fetch crypto data asynchronously
async def get_crypto_data(target_day, period=21):
    load_dotenv()

    api_key = os.getenv("ALPACA_API_KEY")
    api_secret = os.getenv("ALPACA_SECRET")

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
    bars = client.get_crypto_bars(request_params)
    df = bars.df
    return df


async def daily_data_collection():
    # Call both the SMA and RSI functions
    print(f"Starting daily data collection on {datetime.now()}")

    # Fetch the data once
    target_day = "2024-09-21"
    crypto_data = await get_crypto_data(target_day)

    # Calculate the Simple Moving Averages (SMA)
    sma_7, sma_21 = calculateMovingAverage(crypto_data)
    print(f"SMA 7: {sma_7}, SMA 21: {sma_21}")

    # Calculate the RSI
    rsi_value = calculateRSI(crypto_data)
    print(f"RSI: {rsi_value}")

    print(f"Daily data collection completed on {datetime.now()}")


# Running the async function
if __name__ == "__main__":
    asyncio.run(daily_data_collection())
