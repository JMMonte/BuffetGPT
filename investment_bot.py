import pandas as pd
import numpy as np
import yfinance as yf
import os
import pickle

class InvestmentBot:
    def __init__(self):
        self.ledger = self.load_ledger()
        self.tickers = self.get_sp500_tickers()
        self.stock_data = self.load_stock_data()

    # Fetch the list of S&P 500 tickers
    def get_sp500_tickers(self):
        url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
        table = pd.read_html(url, header=0)[0]
        tickers = table['Symbol'].tolist()
        return tickers

    # Load the stock data from a pickle file
    def load_stock_data(self):
        if os.path.exists("data/stock_data.pkl"):
            with open("data/stock_data.pkl", "rb") as f:
                stock_data = pickle.load(f)
            return stock_data
        else:
            return {}
    
    # Save the stock data to a pickle file
    def save_stock_data(self, stock_data):
        with open("data/stock_data.pkl", "wb") as f:
            pickle.dump(stock_data, f)

    # Load the ledger from a pickle file
    def load_ledger(self):
        if os.path.exists("data/ledger.pkl"):
            with open("data/ledger.pkl", "rb") as f:
                self.ledger = pickle.load(f)
        else:
            self.ledger = []

    # Save the ledger to a pickle file
    def save_ledger(self):
        with open("data/ledger.pkl", "wb") as f:
            pickle.dump(self.ledger, f)

    # Fetch historical stock data for the tickers
    def fetch_stock_data(self, tickers):
        stock_data = {}
        for ticker in tickers:
            stock = yf.Ticker(ticker)
            hist_data = stock.history(period="max")
            stock_data[ticker] = hist_data
        return stock_data

    # Filter and sort stocks based on technical indicators
    def dividend_capture_with_technical_analysis(self, stock_data):
        results = []
        for ticker, data in stock_data.items():
            # Calculate technical indicators
            data['rsi'] = self.rsi(data)
            data['macd'], data['signal_line'], data['histogram'] = self.macd(data)
            data['sma'], data['upper_band'], data['lower_band'] = self.bollinger_bands(data)

            # Define your dividend capture strategy logic here
            data['Dividends'] = data['Dividends'].apply(lambda x: x if x > 0 else None)
            dividend_dates = data[data['Dividends'].notnull()].index

            # Dividend capture with technical analysis
            profits = []
            for date in dividend_dates:
                buy_date = date - pd.Timedelta(days=2)
                sell_date = date + pd.Timedelta(days=2)

                if buy_date in data.index and sell_date in data.index:
                    # Technical analysis conditions
                    rsi_condition = data.loc[buy_date]['rsi'] < 30
                    macd_condition = data.loc[buy_date]['macd'] > data.loc[buy_date]['signal_line']
                    bollinger_condition = data.loc[buy_date]['Close'] < data.loc[buy_date]['lower_band']

                    if rsi_condition or macd_condition or bollinger_condition:
                        buy_price = data.loc[buy_date]['Close']
                        sell_price = data.loc[sell_date]['Close']
                        profit = sell_price - buy_price
                        profits.append(profit)

            # Calculate average profit and total profit
            if profits:
                avg_profit = sum(profits) / len(profits)
                total_profit = sum(profits)
                results.append((ticker, avg_profit, total_profit))

        # Sort stocks by total profit
        sorted_stocks = sorted(results, key=lambda x: x[2], reverse=True)
        return sorted_stocks

    # Calculate technical indicators
    def rsi(df, periods=14, ema=True):
        close_delta = df['Close'].diff()
        up = close_delta.clip(lower=0)
        down = -1 * close_delta.clip(upper=0)
        
        if ema:
            ma_up = up.ewm(com=periods-1, adjust=True, min_periods=periods).mean()
            ma_down = down.ewm(com=periods-1, adjust=True, min_periods=periods).mean()
        else:
            ma_up = up.rolling(window=periods, adjust=False).mean()
            ma_down = down.rolling(window=periods, adjust=False).mean()
        
        rsi = ma_up / ma_down
        rsi = 100 - (100/(1 + rsi))
        return rsi

    # Calculate MACD, signal line and histogram
    def macd(df, fast=12, slow=26, signal=9):
        fast_ema = df['Close'].ewm(span=fast, adjust=False).mean()
        slow_ema = df['Close'].ewm(span=slow, adjust=False).mean()
        macd = fast_ema - slow_ema
        signal_line = macd.ewm(span=signal, adjust=False).mean()
        histogram = macd - signal_line
        return macd, signal_line, histogram

    # Calculate Bollinger Bands
    def bollinger_bands(df, window=20, num_std=2):
        rolling_mean = df['Close'].rolling(window).mean()
        rolling_std = df['Close'].rolling(window).std()
        upper_band = rolling_mean + (rolling_std * num_std)
        lower_band = rolling_mean - (rolling_std * num_std)
        return rolling_mean, upper_band, lower_band

    # Execute the investment strategy
    def run_strategy(self):
        stock_data = self.fetch_stock_data(self.tickers)
        self.save_stock_data(stock_data)
        filtered_stocks = self.dividend_capture_with_technical_analysis(stock_data)

        for stock in filtered_stocks:
            ticker, avg_profit, total_profit = stock
            trade = {
                'ticker': ticker,
                'avg_profit': avg_profit,
                'total_profit': total_profit
            }
            self.ledger.append(trade)

        self.save_ledger()

    # Display the performance of the portfolio
    def display_performance(self):
        # Calculate total profit and average profit per trade
        total_profit = sum([trade['total_profit'] for trade in self.ledger])
        avg_profit = total_profit / len(self.ledger) if self.ledger else 0

        # Display the performance
        print("Portfolio Performance:")
        print(f"Total Profit: ${total_profit:.2f}")
        print(f"Average Profit per Trade: ${avg_profit:.2f}")
        print("\nTrade Details:")
        for trade in self.ledger:
            print(f"{trade['ticker']} - Total Profit: ${trade['total_profit']:.2f}, Avg Profit: ${trade['avg_profit']:.2f}")

