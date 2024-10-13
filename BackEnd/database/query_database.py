from datetime import datetime, timedelta
from BackEnd.database.database import get_connection
from BackEnd.utils.compute import compute_all
import pandas as pd


def get_last_trade():
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        query = """
        SELECT trade_id, week_start_date, action, price, quantity, trade_profit_loss, cumulative_profit_loss, decision_date
        FROM weekly_trade_history
        ORDER BY decision_date DESC
        LIMIT 1;
        """
        
        cursor.execute(query)
        row = cursor.fetchone()
        
        
        # Check if any row was returned
        if row:
            # Convert the row to a dictionary for easy access
            last_trade = {
                'trade_id': row['trade_id'],
                'week_start_date': row['week_start_date'],
                'action': row['action'],
                'price': row['price'],
                'quantity': row['quantity'],
                'trade_profit_loss': row['trade_profit_loss'],
                'cumulative_profit_loss': row['cumulative_profit_loss'],
                'decision_date': row['decision_date']
            }
            return last_trade
        else:
            print("No trades found.")
            return None

    except Exception as e:
        print(f"Error fetching last trade: {e}")
        return None

    finally:
        # Ensure the cursor and connection are closed properly
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
        SELECT date, closing_price, sma_7, sma_21, rsi 
        FROM daily_technical_analysis
        WHERE date <= %s
        ORDER BY date DESC 
        LIMIT %s;
        """
        
        cursor.execute(query, (current_date.strftime('%Y-%m-%d'), days))
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


def record_trade_decision(action, date, last_trade, initial_capital=100000):
    conn = get_connection()
    cursor = conn.cursor()
    week_start_date = (datetime.today() - timedelta(days=7)).strftime("%Y-%m-%d")

    today_technical_data = compute_all(date)
    current_price = today_technical_data['close']
    
    # Fetch the last trade to get the previous cumulative P/L and capital
    last_cumulative_pl = last_trade['cumulative_profit_loss'] if last_trade else 0
    last_capital = last_trade['capital'] if last_trade else initial_capital
    
    trade_pl = 0
    quantity = last_trade['quantity']
    
    # Calculate P/L and updated capital
    if action == 'buy':
        quantity = (last_capital * 0.10) / current_price
        trade_pl = 0  # No P/L on a buy, only when sold
        capital_after_trade = last_capital - (current_price * quantity)
        
    elif action == 'sell' and last_trade and last_trade['action'] == 'buy':
        quantity = last_trade['quantity']
        # Calculate P/L based on last buy price
        trade_pl = (current_price - last_trade['price']) * quantity
        capital_after_trade = last_capital + (current_price * quantity) + trade_pl
    else:
        # Hold or unsupported action
        trade_pl = 0
        capital_after_trade = last_capital

    cumulative_pl = last_cumulative_pl + trade_pl

    try:
        query = """
        INSERT INTO weekly_trade_history (week_start_date, action, price, quantity, trade_profit_loss, cumulative_profit_loss, decision_date, capital)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
        """
        values = (week_start_date, action, current_price, quantity, trade_pl, cumulative_pl, capital_after_trade)
        cursor.execute(query, values)
        conn.commit()
        print(f"Recorded trade decision: {action} on {date} with P/L: {trade_pl}, cumulative P/L: {cumulative_pl}, and remaining capital: {capital_after_trade}")
        
    except Exception as e:
        print(f"Error inserting trade decision: {e}")
        
    finally:
        # Ensure the cursor and connection are closed properly
        if cursor:
            cursor.close()
        if conn:
            conn.close()