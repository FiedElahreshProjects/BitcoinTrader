from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from datetime import date
from BackEnd.database.database import get_connection

# Create a router instance for the trading endpoints
router = APIRouter()

class DateRequest(BaseModel):
    date_start: date
    date_end: date

class TradingData(BaseModel):
    trade_id: int
    action: str
    price: float
    quantity: float
    avg_buy_price: float
    trade_profit_loss: float
    cumulative_profit_loss: float
    decision_date: date
    capital: float

@router.get("/get_all_trade_data/", response_model=List[TradingData])
def get_all_trade_data():
    conn = get_connection()
    cursor = conn.cursor()
    try:
        query = """
            SELECT * FROM weekly_trade_history
        """
        cursor.execute(query)
        results = cursor.fetchall()

        if not results:
            raise HTTPException(status_code=404, detail="No trading data found")

        # Map each result to a TechnicalData instance
        technical_data_list = [
            TradingData(
                trade_id=row['trade_id'],
                action=row['action'] ,
                price=row['price'],
                quantity=row['quantity'],
                avg_buy_price=row['avg_buy_price'],
                trade_profit_loss=row['trade_profit_loss'],
                cumulative_profit_loss=row['cumulative_profit_loss'],
                decision_date=row['decision_date'],
                capital=row['capital']
            )
            for row in results
        ]

        return technical_data_list
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server Error: {str(e)}")
    
    finally:
        cursor.close()
        conn.close()
