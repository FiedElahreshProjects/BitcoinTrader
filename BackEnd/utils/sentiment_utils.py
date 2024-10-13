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
        sentiment = analyzer.polarity_scores(f"{post['title']} {post['body']}")
        compound_score = sentiment["compound"]
        positive_score = sentiment["pos"]
        neutral_score = sentiment["neu"]
        negative_score = sentiment["neg"]

        # Weight the scores by the post score
        weighted_compound_scores.append(compound_score * post.score)
        weighted_positive_scores.append(positive_score * post.score)
        weighted_neutral_scores.append(neutral_score * post.score)
        weighted_negative_scores.append(negative_score * post.score)
        total_reddit_score += post.score

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
        raise Exception(f"Failed to store sentiment score: {e}")
    finally:
        cursor.close()
        conn.close()

    # Return the calculated sentiment values
    return round(weighted_compound_score, 5),
        

def calculate_sentiment_wscore(posts: List[RedditPost]):
    if not posts:
        return 0

    positive_scores = []
    neutral_scores = []
    negative_scores = []
    compound_scores = []

    for post in posts:
        sentiment = analyzer.polarity_scores(f"{post['title']} {post['body']}")
        compound_scores.append(sentiment["compound"])
        positive_scores.append(sentiment["pos"])
        neutral_scores.append(sentiment["neu"])
        negative_scores.append(sentiment["neg"])

    # Calculate average scores
    avg_compound_score = sum(compound_scores) / len(compound_scores) if compound_scores else 0
    avg_positive_score = sum(positive_scores) / len(positive_scores) if positive_scores else 0
    avg_neutral_score = sum(neutral_scores) / len(neutral_scores) if neutral_scores else 0
    avg_negative_score = sum(negative_scores) / len(negative_scores) if negative_scores else 0

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
            posts[0]['created'],
            avg_compound_score,
            avg_positive_score,
            avg_neutral_score,
            avg_negative_score
        )
        cursor.execute(query, values)
        result = cursor.fetchone()
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise Exception(f"Failed to store sentiment score: {e}")
    finally:
        cursor.close()
        conn.close()

    # Return the calculated sentiment values
    return round(avg_compound_score, 5),
        
