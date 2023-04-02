import matplotlib.pyplot as plt
import pandas as pd

def plot_stock_data(stock_data, symbol):
    plt.figure(figsize=(12, 6))
    plt.plot(stock_data['Close'], label=f'{symbol} Close Price')
    plt.xlabel('Date')
    plt.ylabel('Close Price')
    plt.title(f'{symbol} Stock Close Price')
    plt.legend()
    plt.show()


def plot_indicator_values(stock_data, indicator_values, symbol, indicator_name):
    plt.figure(figsize=(12, 6))
    plt.plot(stock_data['Close'], label=f'{symbol} Close Price')
    plt.plot(indicator_values, label=f'{indicator_name}')
    plt.xlabel('Date')
    plt.ylabel('Close Price')
    plt.title(f'{symbol} Stock Close Price with {indicator_name}')
    plt.legend()
    plt.show()

def plot_strategy_performance(stock_data, buy_signals, sell_signals, symbol):
    plt.figure(figsize=(12, 6))
    plt.plot(stock_data['Close'], label=f'{symbol} Close Price', alpha=0.7)
    plt.scatter(stock_data.index[buy_signals], stock_data.loc[buy_signals]['Close'], label='Buy', marker='^', color='g', s=100)
    plt.scatter(stock_data.index[sell_signals], stock_data.loc[sell_signals]['Close'], label='Sell', marker='v', color='r', s=100)
    plt.xlabel('Date')
    plt.ylabel('Close Price')
    plt.title(f'{symbol} Stock Close Price with Buy and Sell Signals')
    plt.legend()
    plt.show()
