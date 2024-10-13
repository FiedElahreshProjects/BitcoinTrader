from fastapi import APIRouter, HTTPException, Query
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
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

@router.get("/daily-sentiment/", response_model=DailySentiment)
def get_daily_sentiment_by_date(query_date: date = Query(..., description="The date to fetch sentiment data for")):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        query = "SELECT * FROM daily_sentiment WHERE date = %s"
        cursor.execute(query, (query_date,))
        result = cursor.fetchone()

        if result is None:
            raise HTTPException(status_code=404, detail="No sentiment data found for the given date")

        # Assuming the structure of the query result
        # result = (id, date, positive_score, neutral_score, negative_score, compound_score)
        return DailySentiment(
            date=result[1],
            positive_score=result[2],
            neutral_score=result[3],
            negative_score=result[4],
            compound_score=result[5]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server Error: {str(e)}")
    finally:
        cursor.close()
        conn.close()
