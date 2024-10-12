from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from .database.database import get_connection
from datetime import date
from typing import List


app = FastAPI()

class DailySentiment(BaseModel):
    date: date
    compound_score: float
    positive_score: float = 0
    neutral_score: float = 0
    negative_score: float = 0

@app.get("/")
def read_root():
    return {"message": "Welcome to FastAPI!"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}

@app.post("/daily-sentiment/")
def create_daily_sentiment(sentiment: DailySentiment):
    conn = get_connection()
    #allows direct access to the database
    cursor = conn.cursor()
    try:
        query = """
        INSERT INTO daily_sentiment (date, positive_score, neutral_score, negative_score, compound_score)
        VALUES (%s, %s, %s, %s, %s)
        RETURNING *;
        """
        values = (sentiment.date, sentiment.positive_score, sentiment.neutral_score, sentiment.negative_score, sentiment.compound_score)
        #this is how we run queries via the cursor
        cursor.execute(query, values)
        result = cursor.fetchone()
        #initially make changes with temporary state and not permentanlty applied 
        conn.commit()
    except Exception as e:
        #undos any commited changes on a fail of the operation
        conn.rollback()
        raise HTTPException(status_code=400, detail=f"Failed to insert data: {e}")
    finally:
        cursor.close()
        conn.close()
    
    return result

#response_model = expected data module that will be returned. 
@app.get("/daily-sentiment/", response_model=List[DailySentiment])
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
    
