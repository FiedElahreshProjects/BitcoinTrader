def calculate_rsi(prices, period=14):
    """
    Calculate the Relative Strength Index (RSI) over the specified period.
    
    Args:
        prices (list of float): List of prices.
        period (int): The period over which to calculate RSI, typically 14.

    Returns:
        float: The RSI value.
    """
    if len(prices) < period:
        return None  # Not enough data to calculate RSI

    gains = []
    losses = []

    for i in range(1, len(prices)):
        change = prices[i] - prices[i - 1]
        if change > 0:
            gains.append(change)
        else:
            losses.append(abs(change))

    # Average the gains and losses over the specified period
    average_gain = sum(gains[-period:]) / period if gains else 0
    average_loss = sum(losses[-period:]) / period if losses else 0

    # Prevent division by zero for average_loss
    if average_loss == 0:
        return 100  # If no losses, RSI is 100 (strongly overbought)
    
    rs = average_gain / average_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi
