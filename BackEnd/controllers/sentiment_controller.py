from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from datetime import date
from BackEnd.database.database import get_connection

# Create a router instance for the sentiment endpoints
router = APIRouter()

# Define the Pydantic model for request validation
class DailySentiment(BaseModel):
    date: date
    compound_score: float
    positive_score: float = 0
    neutral_score: float = 0
    negative_score: float = 0

@router.post("/daily-sentiment/")
def create_daily_sentiment(sentiment: DailySentiment):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        query = """
        INSERT INTO daily_sentiment (date, positive_score, neutral_score, negative_score, compound_score)
        VALUES (%s, %s, %s, %s, %s)
        RETURNING *;
        """
        values = (sentiment.date, sentiment.positive_score, sentiment.neutral_score, sentiment.negative_score, sentiment.compound_score)
        cursor.execute(query, values)
        result = cursor.fetchone()
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=f"Failed to insert data: {e}")
    finally:
        cursor.close()
        conn.close()
    
    return result

@router.get("/daily-sentiment/", response_model=List[DailySentiment])
def get_daily_sentiments():
    conn = get_connection()
    cursor = conn.cursor()
    try:
        query = "SELECT * FROM daily_sentiment"
        cursor.execute(query)
        results = cursor.fetchall()
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to retrieve data: {e}")
    finally:
        cursor.close()
        conn.close()

    return results
