from datetime import date
from BackEnd.database.database import get_connection
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from typing import List
from pydantic import BaseModel

# Instantiate the VADER sentiment analyzer
analyzer = SentimentIntensityAnalyzer()

class RedditPost(BaseModel):
    title: str
    body: str
    created: date
    score: int

def calculate_sentiment(posts: List[RedditPost]):
    weighted_compound_scores = []
    weighted_positive_scores = []
    weighted_neutral_scores = []
    weighted_negative_scores = []
    total_reddit_score = 0

    for post in posts:
        # Calculate the sentiment for the post's content
        sentiment = analyzer.polarity_scores(f"{post['title']} {post['body']}")  # Access title and body with dot notation
        compound_score = sentiment["compound"]
        positive_score = sentiment["pos"]
        neutral_score = sentiment["neu"]
        negative_score = sentiment["neg"]

        # Weight the scores by the post score
        weighted_compound_scores.append(compound_score * post['score'])
        weighted_positive_scores.append(positive_score * post['score'])
        weighted_neutral_scores.append(neutral_score * post['score'])
        weighted_negative_scores.append(negative_score * post['score'])
        total_reddit_score += post['score']

    # Calculate the weighted average for each score
    if total_reddit_score > 0:
        weighted_compound_score = sum(weighted_compound_scores) / total_reddit_score
        weighted_positive_score = sum(weighted_positive_scores) / total_reddit_score
        weighted_neutral_score = sum(weighted_neutral_scores) / total_reddit_score
        weighted_negative_score = sum(weighted_negative_scores) / total_reddit_score
    else:
        weighted_compound_score = weighted_positive_score = weighted_neutral_score = weighted_negative_score = 0

    # Database insertion logic
    conn = get_connection()
    cursor = conn.cursor()
    try:
        query = """
        INSERT INTO daily_sentiment (date, compound_score, positive_score, neutral_score, negative_score)
        VALUES (%s, %s, %s, %s, %s)
        RETURNING *;
        """
        values = (
            posts[-1]['created'], 
            weighted_compound_score,
            weighted_positive_score,
            weighted_neutral_score,
            weighted_negative_score
        )
        cursor.execute(query, values)
        result = cursor.fetchone()
        print(result)
        conn.commit()
    except Exception as e:
        conn.rollback()
        print(f"Failed to store sentiment score: {e}")
    finally:
        cursor.close()
        conn.close()

    # Return the calculated sentiment values
    return round(weighted_compound_score, 5)
