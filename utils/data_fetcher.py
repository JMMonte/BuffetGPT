import yfinance as yf
import streamlit as st

@st.cache_data
def fetch_data_for_ticker(ticker, start_date, end_date):
    data = yf.download(ticker, start=start_date, end=end_date)
    return data

def fetch_data(ticker_list, start_date, end_date):
    data = {}
    for ticker in ticker_list:
        data[ticker] = fetch_data_for_ticker(ticker, start_date, end_date)
    return data

