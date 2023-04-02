from visualizations.plots import plot_stock_data, plot_indicator_values, plot_strategy_performance
import streamlit as st
import pandas as pd

def display_stock_data(stock_data, symbol):
    plt = plot_stock_data(stock_data, symbol)
    st.pyplot(plt)

def display_indicator_values(stock_data, indicator_values, symbol, indicator_name):
    plt = plot_indicator_values(stock_data, indicator_values, symbol, indicator_name)
    st.pyplot(plt)

def display_strategy_performance(stock_data, buy_signals, sell_signals, symbol):
    plt = plot_strategy_performance(stock_data, buy_signals, sell_signals, symbol)
    st.pyplot(plt)

st.title('Investabot')
symbol = st.text_input('Enter Stock Symbol:', 'AAPL')
indicator = st.selectbox('Select Indicator:', ('Moving Averages', 'Relative Strength Index (RSI)'))
timeframe = st.selectbox('Select Timeframe:', ('Daily', 'Weekly', 'Monthly'))

if st.button('Analyze'):
    # Fetch stock data and indicator values based on user input
    stock_data = fetch_stock_data(symbol, timeframe)
    indicator_values = calculate_indicator_values(stock_data, indicator)
    
    # Display visualizations
    display_stock_data(stock_data, symbol)
    display_indicator_values(stock_data, indicator_values, symbol, indicator)
