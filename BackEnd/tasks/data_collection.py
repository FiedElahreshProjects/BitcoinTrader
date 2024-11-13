import os
from datetime import datetime
from datetime import timedelta
from alpaca.data.requests import CryptoBarsRequest
from alpaca.data.timeframe import TimeFrame
from alpaca.data.historical import CryptoHistoricalDataClient
from dotenv import load_dotenv
from BackEnd.utils.reddit_data_analysis import reddit_data_analysis
from BackEnd.utils.compute import compute_all

load_dotenv()
api_key = os.getenv("ALPACA_API_KEY")
api_secret = os.getenv("ALPACA_SECRET")

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
    # print(f"Starting daily data collection on {datetime.now()}")

    reddit_data_analysis()

    # Fetch the data once
    try:
        compute_all(datetime.today())
    except Exception as e:
        print(e)

    print(f"Daily data collection completed on {datetime.now()}")



# if __name__ == "__main__":
#     daily_data_collection()