from BackEnd.database.query_database import get_historical_sentiment_data
from BackEnd.database.query_database import get_technical_data
from BackEnd.database.query_database import record_trade_decision, get_technical_by_date, get_historical_sentiment_by_date
from BackEnd.utils.buy_sell_signals import get_sentiment_trade_signal
from BackEnd.utils.buy_sell_signals import get_technical_trade_signal

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
        record_trade_decision('buy', technical_data.iloc[0])
    elif final_decision == 'sell':
        # Record the sell trade
        record_trade_decision('sell', technical_data.iloc[0])
    else:
        print("No action taken (hold).")


def model_load_to_db(date):
    print("Executing autonomous trading logic")
    
    # Get sentiment and technical trade signals
    sentiment_data = get_historical_sentiment_by_date(date)
    sentiment_decision = get_sentiment_trade_signal(sentiment_data=sentiment_data)
    print(f"Sentiment Decision: {sentiment_decision}")
    
    technical_data = get_technical_by_date(date, 4)
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
        record_trade_decision('buy', date, technical_data.iloc[0])
    elif final_decision == 'sell':
        # Record the sell trade
        record_trade_decision('sell', date, technical_data.iloc[0])
    else:
        print("No action taken (hold).")

    

if __name__ == "__main__":
    autonomous_trading_logic()
    