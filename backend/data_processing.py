import pandas as pd
import numpy as np

def calculate_moving_average(stock_data, price_column, window):
    moving_average = stock_data[price_column].rolling(window=window).mean()
    return moving_average

def calculate_rsi(stock_data, price_column, window):
    price_diff = stock_data[price_column].diff()
    gains = price_diff.where(price_diff > 0, 0)
    losses = -price_diff.where(price_diff < 0, 0)
    avg_gain = gains.rolling(window=window).mean()
    avg_loss = losses.rolling(window=window).mean()
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi
