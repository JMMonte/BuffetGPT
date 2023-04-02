import yfinance as yf

def fetch_stock_data(symbol, start, end, interval="1d"):
    stock_data = yf.download(symbol, start=start, end=end, interval=interval)
    return stock_data

