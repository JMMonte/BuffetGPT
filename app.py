import streamlit as st
import pandas as pd
from backend.data_fetching import fetch_sp500_tickers, fetch_dividends, fetch_stock_data
from backend.data_processing import calculate_rsi, filter_stocks_by_rsi, create_portfolio, backtest_strategy
from datetime import datetime, timedelta
from backend.data_processing import get_indicator_values
from visualizations.plots import plot_stock_data, plot_indicator_values, plot_strategy_performance

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

# User Input for Data Fetching
st.subheader('Data Fetching')
start_date = st.date_input('Select Start Date:', datetime(2015, 1, 1))
end_date = st.date_input('Select End Date:', datetime.today())
if st.button('Fetch Data'):
    tickers = fetch_sp500_tickers()
    st.write('Fetching dividend data...')
    # show_progress_bar()
    st.write(f'Progress: {len(tickers) / 503}')
    progress_bar = st.progress(len(tickers) / 503)


    dividend_paying_stocks = fetch_dividends(tickers)
    st.write('Filtering stocks by RSI...')
    selected_stocks = filter_stocks_by_rsi(dividend_paying_stocks, 30, start_date, '1d')
    st.write(f'{len(selected_stocks)} stocks selected for portfolio')

    # Create Portfolio
    initial_capital = st.number_input('Enter your initial capital:', value=10000, min_value=50, step=50)
    num_stocks = st.number_input('Number of stocks you wish to split your capital:', value=5, min_value=1, step=1)
    portfolio_stocks = create_portfolio(selected_stocks, initial_capital, num_stocks)
    st.write(f'Portfolio setup completed with {num_stocks} stocks and initial capital of ${initial_capital}')

    investment_date = st.date_input('Select Investment Date:', datetime.today() - timedelta(days=1))
    st.write(f'Investment started on {investment_date}')

    # Initialize Result Variables
    portfolio_performance = []
    total_earnings = []

    # Run Investment Analysis
    while True:
        st.write('Analyzing portfolio...')

        # Initialize Progress Variables
        num_stocks_analyzed = 0
        total_stocks = len(portfolio_stocks)
        progress_per_stock = 100.0 / total_stocks
        progress = 0

        # Initialize Result Variables
        current_portfolio_value = 0
        total_earnings_today = 0

        # Analyze Each Stock in the Portfolio
        for symbol in portfolio_stocks:
            log_text.write(f'Analyzing {symbol}...')

            # Fetch Stock Data and Indicator Values based on User Input
            stock_data = fetch_stock_data(symbol, start_date, end_date, '1d')
            indicator_values = get_indicator_values(stock_data, 'Relative Strength Index (RSI)')

            # Display Visualizations
            display_stock_data(stock_data, symbol)
            display_indicator_values(stock_data, indicator_values, symbol, 'Relative Strength Index (RSI)')

            # Backtest Investment Strategy
            buy_signals, sell_signals = backtest_strategy(portfolio_stocks, initial_capital, start_date, end_date, interval)

            # Display Performance Summary
            portfolio_performance = backtest_strategy(portfolio_stocks, initial_capital, start_date, end_date, interval)
            total_earnings = (portfolio_performance / 100) * initial_capital
            st.write(f'Performance: {portfolio_performance:.2f}%')
            st.write(f'Earnings: ${total_earnings:.2f} ({(portfolio_performance/100)*initial_capital:.2f}%)')

            # Display Strategy Performance
            display_strategy_performance(stock_data, buy_signals, sell_signals, symbol)

            # Update Progress
            num_stocks_analyzed += 1
            progress = num_stocks_analyzed * progress_per_stock
            progress_bar.progress(progress)
            log_text.write(f'{symbol} analysis complete.')

        # Save Portfolio Data and Stock List
        if st.button('Save Portfolio Data and Stock List'):
            st.write('Saving portfolio data and stock list...')
            # You can add any additional processing/logic here
            st.write('Portfolio data and stock list saved!')

        # Update Portfolio
        if st.button('Update Portfolio'):
            st.write('Updating portfolio...')
            # You can add any additional processing/logic here
            st.write('Portfolio updated!')

        # Divest
        if st.button('Divest'):
            st.write('Divesting portfolio...')
            # You can add any additional processing/logic here
            st.write('Portfolio divested!')

