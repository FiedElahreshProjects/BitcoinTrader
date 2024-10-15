import pandas as pd
from datetime import datetime, timedelta
from BackEnd.tasks.trading import model_load_to_db

def seed_model():
    # Define your start and end dates
    start_date = datetime.strptime("2021-02-12", "%Y-%m-%d")
    end_date = datetime.strptime("2023-04-21", "%Y-%m-%d")
    date_range = pd.date_range(start=start_date, end=end_date)

    # Loop over each date and run the trading logic
    for current_date in date_range:
        # print(current_date)
        # print(f"\nRunning autonomous trading logic for date: {current_date.strftime('%Y-%m-%d')}")

        model_load_to_db(current_date)



if __name__ == "__main__":
    seed_model()
