from typing import List
import praw
import os
import time
from datetime import datetime
from BackEnd.utils.sentiment_utils import calculate_sentiment

reddit = praw.Reddit(
    client_id=os.getenv("CLIENT_ID"),
    client_secret=os.getenv("CLIENT_SECRET"),
    user_agent=os.getenv("USER_AGENT")
)

def get_latest_reddit_posts(subreddit: str):
    subreddit_obj = reddit.subreddit(subreddit)  # Use the user-specified subreddit
    posts = []

    # Get current time in UNIX timestamp and calculate the time for 7 days ago
    current_time = int(time.time())  # Current time in UNIX timestamp
    one_days_ago = current_time - (1 * 24 * 60 * 60)  # Subtract 7 days (in seconds)

    # Fetch the latest 100 posts from the specified subreddit
    for post in subreddit_obj.new(limit=1100):
        # Filter only posts created in the last 7 days
        if post.created_utc >= one_days_ago:
            posts.append({
                "title": post.title,
                "body": post.selftext,
                "created": datetime.utcfromtimestamp(post.created_utc).strftime('%Y-%m-%d'),
                "score": post.score,
            })

    return {"posts": posts}

def reddit_data_analysis():
    posts = get_latest_reddit_posts("Bitcoin")
    return calculate_sentiment(posts)
