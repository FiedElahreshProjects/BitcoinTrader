from datetime import datetime
from BackEnd.database.query_database import get_historical_sentiment_data
from BackEnd.database.query_database import get_technical_data
from BackEnd.database.query_database import record_trade_decision, get_technical_by_date, get_historical_sentiment_by_date
from BackEnd.utils.buy_sell_signals import get_sentiment_trade_signal
from BackEnd.utils.buy_sell_signals import get_technical_trade_signal
from alpaca_trade_api import REST
import os

# Replace with your actual Alpaca API keys


def autonomous_trading_logic():
    print("Executing autonomous trading logic")
    
    # Get sentiment and technical trade signals
    sentiment_data = get_historical_sentiment_data()
    sentiment_decision = get_sentiment_trade_signal(sentiment_data=sentiment_data)
    print(f"Sentiment Decision: {sentiment_decision}")
    
    technical_data = get_technical_data(4)
    technical_decision = get_technical_trade_signal(technical_data=technical_data)
    print(f"Technical Decision: {technical_decision}")
    
    # Determine final trade action based on agreement between indicators
    if sentiment_decision == 'buy' and technical_decision == 'buy':
        final_decision = 'buy'
    elif sentiment_decision == 'sell' and technical_decision == 'sell':
        final_decision = 'sell'
    else:
        final_decision = 'hold'  # If they disagree, we hold

    print(f"Final Trading Decision: {final_decision}")
    
    if final_decision == 'buy':
        # Record the buy trade
        record_trade_decision('buy', date=datetime.today())
    elif final_decision == 'sell':
        # Record the sell trade
        record_trade_decision('sell', date=datetime.today())
    else:
        print("No action taken (hold).")


def model_load_to_db(date: datetime):
    try:
        # Fetch and analyze sentiment and technical signals
        sentiment_data = get_historical_sentiment_by_date(date)
        sentiment_decision = get_sentiment_trade_signal(sentiment_data=sentiment_data)
        
        technical_data = get_technical_by_date(date, 4)
        technical_decision = get_technical_trade_signal(technical_data=technical_data)
        
        # Determine final trade action
        if sentiment_decision == 'buy' and technical_decision == 'buy':
            final_decision = 'buy'
        elif sentiment_decision == 'sell' and technical_decision == 'sell':
            final_decision = 'sell'
        else:
            final_decision = 'hold'
        
        # Record the trade based on the final decision
        if final_decision == 'buy':
            record_trade_decision('buy', date)
        elif final_decision == 'sell':
            record_trade_decision('sell', date)
    
    except Exception as e:
        print(f"Error during model load to DB on {date}: {e}")
