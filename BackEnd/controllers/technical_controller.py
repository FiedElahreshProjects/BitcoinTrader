from fastapi import APIRouter, HTTPException
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from pydantic import BaseModel
from typing import List
from datetime import date
from BackEnd.database.database import get_connection

# Create a router instance for the sentiment endpoints
router = APIRouter()

class DateRequest(BaseModel):
    date: date

class TechnicalData(BaseModel):
    date: date
    closing_price: float
    sma_7: float
    sma_21: float
    rsi: float


# Instantiate the VADER sentiment analyzer
analyzer = SentimentIntensityAnalyzer()

@router.post("/daily-technical-by-date/", response_model=DateRequest)
def get_daily_technical_by_date(date_request: DateRequest):
    date = date_request.date  # Access the date from the request body
    conn = get_connection()
    cursor = conn.cursor()
    try:
        query = "SELECT * FROM daily_technical_analysis WHERE date = %s"
        cursor.execute(query, (date,))
        result = cursor.fetchone()
        print(result)

        if result is None:
            raise HTTPException(status_code=404, detail="No sentiment data found for the given date")

        return TechnicalData(
            date=result['date'],
            closing_price = result['closing_price'],
            sma_7 = result['sma_7'],
            sma_21=result['sma_21'],
            rsi=result['rsi']
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server Error: {str(e)}")
    finally:
        cursor.close()
        conn.close()