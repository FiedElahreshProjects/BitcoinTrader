import pandas as pd
from datetime import datetime
from dotenv import load_dotenv
from BackEnd.utils.sentiment_utils import calculate_sentiment_wscore
from BackEnd.utils.compute import compute_all


load_dotenv()

FILE_PATH = 'C:\\Users\\Fied\\Desktop\\tweets.csv'
CHUNK_SIZE = 100000  # Adjust chunk size based on memory limitations
SKIP_CHUNK = 0
START_ROW = SKIP_CHUNK * CHUNK_SIZE
#Set engine to python if an error with buffer occurs and set memory = True
ENGINE = 'c'
MEMORY = False

def load_sentiment():
# Track overflow posts from the previous chunk
    overflow_posts = []

    # Load data in chunks
    for i, chunk in enumerate(pd.read_csv(FILE_PATH, skiprows=range(1, START_ROW), chunksize=CHUNK_SIZE, low_memory=MEMORY, on_bad_lines='skip', engine=ENGINE)):
        if(i >= 60):
            break
        print(f"Processing chunk {SKIP_CHUNK + i + 1}...")

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
    load_sentiment()
    
    # Define the date range from 2021-02-01 to the end of 2022
    start_date = "2021-12-31"
    end_date = "2023-06-21"
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
