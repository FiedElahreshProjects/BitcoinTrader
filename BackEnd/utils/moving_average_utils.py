def calculate_moving_average(prices, period):
    """
    Calculate the simple moving average over the specified period.
    
    Args:
        prices (list of float): List of prices.
        period (int): The number of prices to average.

    Returns:
        float: The moving average, or None if there aren't enough data points.
    """
    if len(prices) < period:
        return None  # Not enough data to calculate moving average
    return sum(prices[-period:]) / period
