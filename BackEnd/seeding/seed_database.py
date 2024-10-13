import pandas as pd
from datetime import datetime
from dotenv import load_dotenv
from BackEnd.utils.sentiment_utils import calculate_sentiment_wscore
from BackEnd.utils.compute import compute_all

load_dotenv()

file_path = '/Users/avnoorludhar/Desktop/Bitcoin_tweets.csv'
chunk_size = 100000  # Adjust chunk size based on memory limitations

def load_sentiment():
# Track overflow posts from the previous chunk
    overflow_posts = []

    # Load data in chunks
    for i, chunk in enumerate(pd.read_csv(file_path, chunksize=chunk_size, low_memory=False)):
        if(i >= 45):
            break
        print(f"Processing chunk {i + 1}...")

        # Convert the date column to datetime and drop invalid dates
        chunk['date'] = pd.to_datetime(chunk['date'], errors='coerce')
        #drops NaN values in the date column
        valid_chunk = chunk.dropna(subset=['date'])

        # Merge overflow posts from previous chunk to ensure no segmentation of dates
        chunk_posts = pd.concat([pd.DataFrame(overflow_posts), valid_chunk], ignore_index=True)
        chunk_posts = chunk_posts.sort_values(by='date').reset_index(drop=True)
        overflow_posts = []
        j = 0

        # Group by date and accumulate posts
        #.dt.date returns the date from the datatime data in pandas
        for date, group in chunk_posts.groupby(chunk_posts['date'].dt.date):
            posts = []
            print(date)

            for _, row in group.iterrows():
                posts.append({
                    'title': '',
                    'body': row.get('text', ''),
                    'created': date,
                    'score': 0 # Assuming retweets act as score
                })

            
            if j == len(chunk_posts.groupby(chunk_posts['date'].dt.date)) - 1:
                # Save any remaining posts for the next chunk as overflow
                overflow_posts = chunk_posts.iloc[group.index[-1] + 1:].to_dict('records')
                break  # Stop here to continue in the next chunk

            # Process sentiment analysis
            if posts:
                try:
                    sentiment_score = calculate_sentiment_wscore(posts)
                    print(f"Sentiment for {date}: {sentiment_score}")
                except Exception as e:
                    print(e)
            
            j += 1


def seed_sentiment_data():
    # load_sentiment()
    
    # Define the date range from 2021-02-01 to the end of 2022
    start_date = "2022-04-01"
    end_date = "2023-11-21"
    date_range = pd.date_range(start=start_date, end=end_date)

    # Loop over each date and call compute_all
    for date in date_range:
        try:
            result = compute_all(date)
            print(f"Computed indicators for {date.date()}: {result}")
        except Exception as e:
            print(f"Error on {date.date()}: {e}")


if __name__ == "__main__":
    seed_sentiment_data()
