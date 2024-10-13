from dotenv import load_dotenv
import os
import pandas as pd
from datetime import datetime, timedelta
from BackEnd.database.database import get_connection
from BackEnd.utils.sentiment_utils import calculate_sentiment
from BackEnd.utils.reddit_data_analysis import reddit_data_analysis

load_dotenv()

file_path = 'Bitcoin_tweets.csv'
chunk_size = 10000  # Size of each chunk

def seed_sentiment_data():
    conn = get_connection()
    cursor = conn.cursor()

    # Load data in chunks
    for i, chunk in enumerate(pd.read_csv(file_path, chunksize=chunk_size)):
        print(f"Processing chunk {i + 1}...")

        # Convert the date column to datetime, handle parsing errors
        chunk['date'] = pd.to_datetime(chunk['date'], errors='coerce')  # Coerce invalid dates to NaT

        # Filter rows where 'date' is valid
        valid_chunk = chunk.dropna(subset=['date'])

        # Group by date and accumulate posts
        for date, group in valid_chunk.groupby(valid_chunk['date'].dt.date):
            posts = []

            # Create a list of posts from the chunk
            for _, row in group.iterrows():
                posts.append({
                    'title': row.get('title', ''),
                    'body': row.get('text', ''),
                    'created': date,
                    'score': row.get('retweets', 0)  # Assuming retweets act as score
                })

            # Calculate sentiment for the day's posts and store it in the database
            if posts:
                sentimentresult = calculatesentiment2(posts)
                print(f"Sentiment for {date}: {sentimentresult}")

if __name__ == "__main":
    seed_sentiment_data()
