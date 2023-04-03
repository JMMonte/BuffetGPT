import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import yfinance as yf
from backend import data_fetching as fetch_stock_data

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

def get_indicator_values(stock_data, indicator):
    if indicator == 'Moving Averages':
        # Calculate moving average with a specified window (e.g., 20 days)
        return calculate_moving_average(stock_data, 'Close', 20)
    elif indicator == 'Relative Strength Index (RSI)':
        # Calculate RSI with a specified window (e.g., 14 days)
        return calculate_rsi(stock_data, 'Close', 14)
    else:
        raise ValueError(f"Invalid indicator: {indicator}")

def filter_stocks_by_rsi(stocks, rsi_threshold, start_date, timeframe):
    selected_stocks = []
    for stock in stocks:
        stock_data = fetch_stock_data(stock, start_date, datetime.now().strftime('%Y-%m-%d'), timeframe)

        rsi_values = calculate_rsi(stock_data, 'Close', 14)
        if rsi_values.iloc[-1] <= rsi_threshold:
            selected_stocks.append(stock)
    return selected_stocks

def create_portfolio(stocks, capital, num_stocks):
    portfolio = {}
    stocks_to_invest = min(len(stocks), num_stocks)
    capital_per_stock = capital / stocks_to_invest

    for stock in stocks[:stocks_to_invest]:
        stock_data = yf.Ticker(stock)
        current_price = stock_data.info['regularMarketPrice']
        shares = capital_per_stock // current_price
        portfolio[stock] = shares

    return portfolio

def backtest_strategy(portfolio, start_date, end_date, timeframe):
    initial_value = 0
    final_value = 0

    for stock, shares in portfolio.items():
        stock_data = fetch_stock_data(stock, start_date, end_date, timeframe)
        initial_price = stock_data['Close'][0]
        final_price = stock_data['Close'][-1]
        initial_value += shares * initial_price
        final_value += shares * final_price

    performance = ((final_value - initial_value) / initial_value) * 100
    return performance

def update_portfolio(portfolio, capital, num_stocks):
    updated_portfolio = {}
    stocks_to_invest = min(len(portfolio), num_stocks)
    capital_per_stock = capital / stocks_to_invest

    for stock, shares in portfolio.items():
        stock_data = yf.Ticker(stock)
        current_price = stock_data.info['regularMarketPrice']
        updated_shares = capital_per_stock // current_price
        updated_portfolio[stock] = updated_shares

    return updated_portfolio
