from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import List
from datetime import date
from BackEnd.database.database import get_connection

# Create a router instance for the technicals endpoints
router = APIRouter()

class DateRequest(BaseModel):
    date_start: date
    date_end: date

class TechnicalData(BaseModel):
    date: date
    closing_price: float
    sma_7: float
    sma_21: float
    rsi: float

@router.post("/daily-technical-by-date/", response_model=List[TechnicalData])
def get_daily_technical_by_date(date_request: DateRequest):
    date_start = date_request.date_start
    date_end = date_request.date_end
    conn = get_connection()
    cursor = conn.cursor()
    try:
        query = """
            SELECT date, closing_price, sma_7, sma_21, rsi 
            FROM daily_technical_analysis 
            WHERE date >= %s AND date <= %s
        """
        cursor.execute(query, (date_start, date_end))
        results = cursor.fetchall()

        if not results:
            raise HTTPException(status_code=404, detail="No technical data found for the given date range")

        # Map each result to a TechnicalData instance
        technical_data_list = [
            TechnicalData(
                date=row['date'],
                closing_price=row['closing_price'],
                sma_7=row['sma_7'],
                sma_21=row['sma_21'],
                rsi=row['rsi']
            )
            for row in results
        ]

        return technical_data_list

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server Error: {str(e)}")
    
    finally:
        cursor.close()
        conn.close()
