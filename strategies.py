import pandas as pd
import numpy as np
from ta.momentum import RSIIndicator
from ta.volatility import BollingerBands

def moving_average_strategy(df, short_window=10, long_window=30):
    # Calculate the moving averages
    df['Short_MA'] = df['Close'].rolling(window=short_window).mean()
    df['Long_MA'] = df['Close'].rolling(window=long_window).mean()

    # Generate buy and sell signals
    df['Buy'] = (df['Short_MA'] > df['Long_MA']) & (df['Short_MA'].shift(1) <= df['Long_MA'].shift(1))
    df['Sell'] = (df['Short_MA'] < df['Long_MA']) & (df['Short_MA'].shift(1) >= df['Long_MA'].shift(1))

def momentum_strategy(df, rsi_period=14, rsi_min=30, rsi_max=70):
    # Calculate RSI
    rsi = RSIIndicator(df['Close'], rsi_period)
    df['RSI'] = rsi.rsi()

    # Generate buy and sell signals
    df['Buy'] = (df['RSI'] < rsi_min)
    df['Sell'] = (df['RSI'] > rsi_max)

def bollinger_bands_strategy(df, window=20, num_of_std=2):
    # Calculate Bollinger Bands
    bollinger = BollingerBands(df['Close'], window, num_of_std)
    df['Upper_BB'] = bollinger.bollinger_hband()
    df['Lower_BB'] = bollinger.bollinger_lband()

    # Generate buy and sell signals
    df['Buy'] = (df['Close'] < df['Lower_BB'])
    df['Sell'] = (df['Close'] > df['Upper_BB'])
