from fastapi import FastAPI, Query
import praw
import time
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

app = FastAPI()
load_dotenv()

# Reddit API authentication using PRAW
reddit = praw.Reddit(
    client_id=os.getenv("CLIENT_ID"),
    client_secret=os.getenv("CLIENT_SECRET"),
    user_agent=os.getenv("USER_AGENT")
)


@app.get("/reddit")
def get_reddit_posts(subreddit: str = Query(..., description="The subreddit to fetch posts from")):
    # Calculate the UNIX timestamps for one week ago and the current time
    current_time = int(time.time())  # Current time in UNIX timestamp
    one_week_ago = current_time - (7 * 24 * 60 * 60)  # One week ago in UNIX timestamp

    # Access the subreddit
    subreddit_obj = reddit.subreddit(subreddit)

    # Fetch the latest posts within the last week
    posts = []
    for post in subreddit_obj.new(limit=100):  # Adjust limit as needed
        if one_week_ago <= post.created_utc <= current_time:
            posts.append({
                "post_title": post.title,
                "post_body": post.selftext,
                "post_score": post.score,
            })

    return {"posts": posts}
