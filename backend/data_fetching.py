import requests
from bs4 import BeautifulSoup
import pandas as pd
import yfinance as yf

def fetch_sp500_tickers():
    url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.find('table', {'class': 'wikitable'})
    tickers = []
    for row in table.findAll('tr')[1:]:
        ticker = row.findAll('td')[0].text.strip()
        tickers.append(ticker)
        print(f"Found ticker: {ticker}")
    return tickers

def fetch_dividends(tickers):
    dividend_paying_stocks = []
    for ticker in tickers:
        stock_data = yf.Ticker(ticker)
        dividend_history = stock_data.dividends
        if isinstance(dividend_history, pd.DataFrame) and not dividend_history.empty:
            dividend_paying_stocks.append(ticker)
            print(f"{ticker} pays dividends")
    return dividend_paying_stocks

def fetch_stock_data(symbol, start_date, end_date, interval):
    stock_data = yf.download(symbol, start=start_date, end=end_date, interval=interval)
    return stock_data
