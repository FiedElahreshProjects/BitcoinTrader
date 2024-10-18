from BackEnd.database.query_database import get_last_trade

def get_technical_trade_signal(technical_data):
    # Get the latest RSI, 7-day SMA, and 21-day SMA values
    latest_rsi = technical_data['rsi'].iloc[-1]
    sma_7_current = technical_data['sma_7'].iloc[-1]
    sma_21_current = technical_data['sma_21'].iloc[-1]
    
    # # Get previous day SMA values to detect a crossover
    # sma_7_previous = technical_data['sma_7'].iloc[-2]
    # sma_21_previous = technical_data['sma_21'].iloc[-2]
    
    # Calculate more sensitive RSI thresholds
    buy_rsi_threshold = 48  # Increased sensitivity for buy signals
    sell_rsi_threshold = 52  # Increased sensitivity for sell signals
    
    # Determine Buy Signal
    if latest_rsi < buy_rsi_threshold and sma_7_current >= sma_21_current:
        return 'buy'
    
    # Determine Sell Signal
    elif latest_rsi > sell_rsi_threshold and sma_7_current < sma_21_current:
        return 'sell'
    
    # If no signals, hold
    else:
        return 'hold'



def get_sentiment_trade_signal(sentiment_data):
    # Convert compound_score to float to avoid type errors
    sentiment_data['compound_score'] = sentiment_data['compound_score'].astype(float)
    
    # Calculate moving average and standard deviation
    mean_sentiment = sentiment_data['compound_score'].mean()
    std_dev_sentiment = sentiment_data['compound_score'].std()
    
    # Latest sentiment score
    latest_sentiment = sentiment_data['compound_score'].iloc[-1]
    
    # Calculate very sensitive Bollinger Bands (0.5 standard deviations)
    upper_band = mean_sentiment + 0.5 * std_dev_sentiment
    lower_band = mean_sentiment - 0.5 * std_dev_sentiment

    # Calculate a very sensitive z-score threshold (e.g., 0.25)
    z_score = (latest_sentiment - mean_sentiment) / std_dev_sentiment
    
    # Define extremely sensitive thresholds for buy and sell signals
    buy_z_threshold = 0.25  # Very sensitive threshold for buy signals
    sell_z_threshold = -0.25  # Very sensitive threshold for sell signals

    # Determine trade signal based on highly sensitive thresholds
    if latest_sentiment > upper_band and z_score >= buy_z_threshold:
        return 'buy'  # Buy on slight positive sentiment
    elif latest_sentiment < lower_band and z_score <= sell_z_threshold:
        return 'sell'  # Sell on slight negative sentiment
    else:
        return 'hold'
