from dotenv import load_dotenv
import os
import random
import requests
from datetime import datetime, timedelta
from BackEnd.database.database import get_connection
from BackEnd.tasks.data_collection import reddit_data_analysis

load_dotenv()

def seed_sentiment_data():
    conn = get_connection()
    cursor = conn.cursor()

    end_date = datetime.now()
    start_date = end_date - timedelta(days=90)

    current_date = start_date
    while(current_date <= end_date):
        print(reddit_data_analysis())
    

if __name__ == "__main__":
    seed_sentiment_data()
