from datetime import datetime, timedelta
from typing import Optional
from pydantic import BaseModel
from BackEnd.database.database import get_connection
from BackEnd.utils.compute import compute_all_wo_insert
import pandas as pd
from typing import Optional

class Trade(BaseModel):
    action: str
    price: float
    quantity: float
    trade_profit_loss: float
    cumulative_profit_loss: float
    decision_date: datetime
    capital: float
    avg_buy_price: float  # New field to store the average buy price


def get_last_trade(trade_date: datetime) -> Optional[Trade]:
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        query = """
        SELECT action, price, quantity, trade_profit_loss, cumulative_profit_loss, decision_date, capital, avg_buy_price
        FROM weekly_trade_history
        WHERE decision_date < %s
        ORDER BY decision_date DESC
        LIMIT 1;
        """
        
        cursor.execute(query, (trade_date,))
        row = cursor.fetchone()
        
        if row:
            last_trade = Trade(
                action=row['action'],
                price=row['price'],
                quantity=row['quantity'],
                trade_profit_loss=row['trade_profit_loss'],
                cumulative_profit_loss=row['cumulative_profit_loss'],
                decision_date=row['decision_date'],
                capital=row['capital'],
                avg_buy_price=row['avg_buy_price']  # Include the avg_buy_price field
            )
            return last_trade
        else:
            # Return None if no trade is found
            return None

    except Exception as e:
        print(f"Error fetching last trade: {e}")
        raise  # Re-raise the exception to propagate the error
    
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def get_historical_sentiment_data(days=7):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        query = f"""
        SELECT date, compound_score 
        FROM daily_sentiment
        ORDER BY date DESC 
        LIMIT {days};
        """
        
        cursor.execute(query)
        rows = cursor.fetchall()
        
        # Convert to DataFrame
        df = pd.DataFrame(rows, columns=['date', 'compound_score'])
        return df

    except Exception as e:
        print(f"Error fetching sentiment data: {e}")
        return pd.DataFrame()  # Return an empty DataFrame if there's an error

    finally:
        # Ensure the cursor and connection are closed properly
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def get_technical_data(days: int):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        query = f"""
        SELECT date, closing_price, sma_7, sma_21, rsi 
        FROM daily_technical_analysis
        ORDER BY date DESC LIMIT {days};
        """
        
        cursor.execute(query)
        rows = cursor.fetchall()
        
        # Convert to DataFrame
        df = pd.DataFrame(rows, columns=['date', 'closing_price', 'sma_7', 'sma_21', 'rsi'])
        return df
    except Exception as e:
        print(f"Error fetching technical data: {e}")
        return pd.DataFrame()  # Return an empty DataFrame if there's an error
    finally:
        # Ensure the cursor and connection are closed properly
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def get_historical_sentiment_by_date(date: datetime, days: int = 7):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        date = date.strftime('%Y-%m-%d')
        
        query = f"""
        SELECT date, compound_score 
        FROM daily_sentiment
        WHERE date <= %s
        ORDER BY date DESC 
        LIMIT %s;
        """
        
        cursor.execute(query, (date, days))
        rows = cursor.fetchall()
        
        # Convert to DataFrame
        df = pd.DataFrame(rows, columns=['date', 'compound_score'])
        return df

    except Exception as e:
        print(f"Error fetching sentiment data: {e}")
        return pd.DataFrame()  # Return an empty DataFrame if there's an error

    finally:
        # Ensure the cursor and connection are closed properly
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def get_technical_by_date(current_date: datetime, days: int):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        query = f"""
        SELECT *
        FROM daily_technical_analysis
        WHERE date <= %s
        ORDER BY date DESC 
        LIMIT %s;
        """
        
        cursor.execute(query, (current_date.strftime('%Y-%m-%d'), days))
        rows = cursor.fetchall()
        
        # Convert to DataFrame
        df = pd.DataFrame(rows, columns=['date', 'closing_price', 'sma_7', 'sma_21', 'rsi', 'capital', 'quantity', 'cumulative_profit_loss', 'action', 'price'])
        return df

    except Exception as e:
        print(f"Error fetching technical data: {e}")
        return pd.DataFrame()  # Return an empty DataFrame if there's an error

    finally:
        # Ensure the cursor and connection are closed properly
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def record_trade_decision(action: str, date: datetime, initial_capital=100000):
    conn = get_connection()
    cursor = conn.cursor()
    
    date_technical_data = compute_all_wo_insert(date)
    current_price = date_technical_data.closing_price  # No rounding here yet

    last_trade = get_last_trade(date)
    
    # Initialize variables based on the last trade or set default values
    last_cumulative_pl = last_trade.cumulative_profit_loss if last_trade else 0
    last_capital = last_trade.capital if last_trade else initial_capital
    quantity = last_trade.quantity if last_trade else 0
    avg_buy_price = last_trade.avg_buy_price if last_trade else 0
    trade_pl = 0
    capital_after_trade = last_capital
    
    # Buy logic with average price calculation
    if action == 'buy':
        buy_quantity = (last_capital * 0.10) / current_price  # Full precision quantity for buy
        buy_cost = current_price * buy_quantity
        
        if last_capital >= buy_cost:
            # Update the weighted average price of BTC
            total_cost = (avg_buy_price * quantity) + buy_cost
            quantity += buy_quantity
            avg_buy_price = total_cost / quantity  # Update to the new weighted average price
            
            capital_after_trade = last_capital - buy_cost
        else:
            print("Insufficient capital for buy action.")
            return

    # Sell logic: Sell the entire position
    elif action == 'sell':
        if quantity > 0:
            # Sell the entire quantity
            trade_pl = (current_price - avg_buy_price) * quantity  # P/L based on the average price
            capital_after_trade = last_capital + (current_price * quantity) + trade_pl
            
            # After selling, reset quantity and avg_buy_price to zero since we no longer hold any position
            quantity = 0
            avg_buy_price = 0
        else:
            print("No quantity to sell; cannot execute sell action.")
            return

    # Update cumulative profit/loss
    cumulative_pl = last_cumulative_pl + trade_pl  # Full precision cumulative P/L

    try:
        # Update database query to include avg_buy_price
        query = """
        INSERT INTO weekly_trade_history (action, price, quantity, trade_profit_loss, cumulative_profit_loss, decision_date, capital, avg_buy_price)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
        """
        # Round only when storing in the database
        values = (
            action,
            round(current_price, 2),
            round(quantity, 4),
            round(trade_pl, 2),
            round(cumulative_pl, 2),
            date,
            round(capital_after_trade, 2),
            round(avg_buy_price, 2)
        )
        cursor.execute(query, values)
        conn.commit()
        print(f"Recorded trade decision: {action} on {date} with P/L: {round(trade_pl, 2)}, cumulative P/L: {round(cumulative_pl, 2)}, and remaining capital: {round(capital_after_trade, 2)}")
        
    except Exception as e:
        print(f"Error inserting trade decision: {e}")
        
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()