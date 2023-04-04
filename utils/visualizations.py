import matplotlib.pyplot as plt
import pandas as pd

def calculate_portfolio_value(investment_log, data):
    portfolio_value = []
    for entry in investment_log:
        date = entry['date']
        total_value = 0
        for order in entry['orders']:
            ticker = order['ticker']
            shares = order['shares']
            stock_data = data[ticker].loc[data[ticker].index <= date]
            if len(stock_data) > 0:
                price = stock_data['Close'].iloc[-1]
                total_value += shares * price
        portfolio_value.append((date, total_value))
    return portfolio_value
