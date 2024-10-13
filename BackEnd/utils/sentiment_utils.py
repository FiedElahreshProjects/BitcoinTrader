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
    weighted_scores = []
    total_reddit_score = 0

    for post in posts:
        # Calculate the sentiment for the post's content
        compound_score = analyzer.polarity_scores(f"{post['title']} {post['body']}")["compound"]
        weighted_score = compound_score * post['score']
        weighted_scores.append(weighted_score)
        total_reddit_score += post['score']

    # Calculate the weighted average compound score
    if total_reddit_score > 0:
        weighted_compound_score = sum(weighted_scores) / total_reddit_score
    else:
        weighted_compound_score = 0
    
    # Database insertion logic
    conn = get_connection()
    cursor = conn.cursor()
    try:
        query = """
        INSERT INTO daily_sentiment (date, compound_score)
        VALUES (%s, %s)
        RETURNING *;
        """
        values = (posts[-1]['created'], weighted_compound_score)
        cursor.execute(query, values)
        result = cursor.fetchone()
        print(result)
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise Exception(f"Failed to store sentiment score: {e}")
    finally:
        cursor.close()
        conn.close()
    
    # Return the calculated sentiment and result from the database
    return round(weighted_compound_score, 5)

def calculate_sentiment_wscore(posts):
    if not posts:
        return 0  # Handle case where no posts are available

    # Calculate the average sentiment score for posts
    sentiments = [analyzer.polarity_scores(f"{post['title']} {post['body']}")["compound"] for post in posts]
    compound_score = sum(sentiments) / len(sentiments) if len(sentiments) > 0 else 0

    # Database insertion logic
    conn = get_connection()
    cursor = conn.cursor()
    try:
        query = """
            INSERT INTO daily_sentiment (date, compound_score)
            VALUES (%s, %s)
            RETURNING *;
            """
        values = (posts[0]['created'], compound_score)
        cursor.execute(query, values)
        result = cursor.fetchone()
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise Exception(f"Failed to store sentiment score: {e}")
    finally:
        cursor.close()
        conn.close()

    # Return the calculated sentiment and result from the database
    return round(compound_score, 5)
