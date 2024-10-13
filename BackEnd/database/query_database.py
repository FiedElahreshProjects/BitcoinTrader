from datetime import datetime, timedelta
from BackEnd.database.database import get_connection
from BackEnd.utils.compute import compute_all, compute_all_wo_insert
import pandas as pd


def get_last_trade(trade_date):
    conn = get_connection()
    # Use RealDictCursor to get results as dictionaries
    cursor = conn.cursor()
    
    try:
        query = """
        SELECT trade_id, week_start_date, action, price, quantity, trade_profit_loss, cumulative_profit_loss, decision_date
        FROM weekly_trade_history
        WHERE decision_date < %s
        ORDER BY decision_date DESC
        LIMIT 1;
        """
        
        cursor.execute(query, (trade_date,))
        row = cursor.fetchone()
        
        # Check if any row was returned
        if row:
            # row is now a dictionary, so you can access fields by column name
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


def record_trade_decision(action, date, initial_capital=100000):
    conn = get_connection()
    cursor = conn.cursor()
    
    # Now perform the date arithmetic
    week_start_date = (date - timedelta(days=7)).strftime("%Y-%m-%d")
    if(isinstance(date, pd.Timestamp)):
        date = date.to_pydatetime() # Convert date to string for use later
        
    
    last_trade = get_last_trade(date)

    today_technical_data = compute_all_wo_insert(date)
    current_price = today_technical_data['closing_price']
    last_cumulative_pl = last_trade.get('cumulative_profit_loss', 0) if last_trade else 0
    last_capital = last_trade.get('capital', initial_capital) if last_trade else initial_capital
    quantity = last_trade.get('quantity', 0) if last_trade else 0
    
    
    # Calculate P/L and updated capital
    if action == 'buy':
        print(last_capital)
        quantity += (last_capital * 0.10) / current_price
        trade_pl = 0  # No P/L on a buy, only when sold
        print(last_capital)
        if(last_capital - (current_price * quantity) >= 0):
            capital_after_trade = last_capital - (current_price * quantity)
        else:
            return
    elif action == 'sell' and last_trade['action'] == 'buy':
        quantity -= last_trade['quantity']
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
        values = (week_start_date, action, current_price, quantity, trade_pl, cumulative_pl, date, capital_after_trade)
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

