import numpy as np
import pandas as pd
import yfinance as yf

class InvestmentBot:
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

    def macd(df, fast=12, slow=26, signal=9):
        fast_ema = df['Close'].ewm(span=fast, adjust=False).mean()
        slow_ema = df['Close'].ewm(span=slow, adjust=False).mean()
        macd = fast_ema - slow_ema
        signal_line = macd.ewm(span=signal, adjust=False).mean()
        histogram = macd - signal_line
        return macd, signal_line, histogram

    def bollinger_bands(df, window=20, num_std=2):
        rolling_mean = df['Close'].rolling(window).mean()
        rolling_std = df['Close'].rolling(window).std()
        upper_band = rolling_mean + (rolling_std * num_std)
        lower_band = rolling_mean - (rolling_std * num_std)
        return rolling_mean, upper_band, lower_band
    
    def filter_and_sort_stocks(self, stock_data):
        results = []
        for ticker, data in stock_data.items():
            # Calculate technical indicators
            data['rsi'] = self.rsi(data)
            data['macd'], data['signal_line'], data['histogram'] = self.macd(data)
            data['sma'], data['upper_band'], data['lower_band'] = self.bollinger_bands(data)

            # Define entry and exit rules
            data['long_entry'] = ((data['rsi'] < 30) | (data['macd'] > data['signal_line']) | (data['Close'] < data['lower_band']))
            data['long_exit'] = ((data['rsi'] > 70) | (data['macd'] < data['signal_line']) | (data['Close'] > data['upper_band']))

            # Calculate returns
            data['position'] = data['long_entry'].cumsum() - data['long_exit'].cumsum()
            data['position'] = data['position'].clip(lower=0)
            data['returns'] = data['Close'].pct_change() * data['position']

            # Calculate average profit and total profit
            profits = data['returns'].dropna().tolist()
            if profits:
                avg_profit = np.mean(profits)
                total_profit = np.sum(profits)
                results.append((ticker, avg_profit, total_profit))

        # Sort stocks by total profit
        sorted_stocks = sorted(results, key=lambda x: x[2], reverse=True)
        return sorted_stocks

# Get stock data
symbol = 'AAPL'
df = yf.download(symbol)

# Calculate indicators
df['rsi'] = InvestmentBot.rsi(df)
df['macd'], df['signal_line'], df['histogram'] = InvestmentBot.macd(df)
df['sma'], df['upper_band'], df['lower_band'] = InvestmentBot.bollinger_bands(df)

# Define entry and exit rules
df['long_entry'] = ((df['rsi'] < 30) | (df['macd'] > df['signal_line']) | (df['Close'] < df['lower_band']))
df['long_exit'] = ((df['rsi'] > 70) | (df['macd'] < df['signal_line']) | (df['Close'] > df['upper_band']))

# Calculate returns
df['position'] = df['long_entry'].cumsum() - df['long_exit'].cumsum()
df['position'] = df['position'].clip(lower=0)
df['returns'] = df['Close'].pct_change() * df['position']

# Print results
print('Data:')
print(df.tail())
print()

# Calculate performance
performance = (1 + df['returns']).cumprod().iloc[-1] - 1
print(f'Performance: {performance:.2%}')