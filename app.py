import streamlit as st  # Import the streamlit library
import yfinance as yf
import pandas as pd
import ta  # Import the technical analysis library
import plotly.express as px
from datetime import datetime
from datetime import timedelta
import re  # Import the regular expression library

# Define the stock symbol validator
def is_valid_stock_symbol(symbol):
  return re.match(r"^[A-Za-z0-9\.\-\^]+$", symbol) is not None

# Time variables
now = datetime.now()
current_time = now.strftime("%H:%M:%S")
today = now.strftime("%d %B %Y")
time_ago = now - timedelta(days=120)

# Just a nice URL
url = "https://www.investopedia.com/terms/r/rsi.asp"

# Set the title of the app
st.title("Technical Analysis Investment Bot")
warning = st.warning(
  "👈 Your portfolio data will go here. Setup the bot in the side bar")

# Open the sidebar
with st.sidebar:
  with st.expander("About this bot"):
    st.write(
      '''This is a simple backtesting sandbox that uses Yfinance history data to preform technical analysis, set a list of buy and sell orders and plot the resutl. It's pretty simple.
      For technical analysis, this bot uses RSI, or Relative Strength Index, which is a measure of the change in price over a period of time.
      More about RSI here: [Investopedia](%s)''' % url)
  # Input the total amount of money to be invested
  total_investment = st.number_input(
    "Enter the total amount of money to be invested:",
    min_value=0.0,
    value=10000.0,
    step=1.0)

  # Input the stock symbol and date range for backtesting
  symbol = st.text_input("Enter the stock symbol (e.g., AAPL):", "AAPL")
  try:
    if not symbol:
      raise ValueError
  except ValueError:
    st.error("Please enter a stock symbol.")

  # Set the backtesting parameters
  start_date = st.date_input("Start date for backtesting:",
                             value=pd.to_datetime(time_ago))
  end_date = st.date_input("End date for backtesting:",
                           value=pd.to_datetime(today))
  # Set the min RSI value
  rsi_min = st.number_input(
    "Enter the minimum RSI value:",
    min_value=0.0,
    value=30.0,
    step=0.1,
    help=
    "The RSI is a measure of the change in price over a period of time. A normal minimum value for a stock is 30 or less. For ETFs and index, use a value of 45 or 35."
  )
  # Set the max RSI value
  rsi_max = st.number_input(
    "Enter the maximum RSI value:",
    min_value=0.0,
    value=70.0,
    step=0.1,
    help=
    "The RSI is a measure of the change in price over a period of time. A normal maximum value for a stock is 70 or more. For ETFs and index, use a value of 55 or 60."
  )

  # Fetch historical data using yfinance
  data = yf.download(symbol, start=start_date, end=end_date, interval="1d")

  # Create a "Start Bot" button
  start_bot_button = st.button("Start Bot")

# Execute the following code only when the button is pressed
if start_bot_button:
  warning = st.empty()
  # Split the input symbols into a list
  symbols_list = symbol.split(',')

  # Initialize an empty DataFrame to store historical data
  data = pd.DataFrame()

  # Fetch historical data for each symbol and concatenate them into one DataFrame
  for symbol in symbols_list:
    symbol_data = yf.download(symbol,
                              start=start_date,
                              end=end_date,
                              interval="1d")
    symbol_data['Symbol'] = symbol
    data = pd.concat([data, symbol_data])

  # Check if data is available
  if data.empty:
    st.write(
      "No data available for the provided stock symbols and date range.")
  else:
    # Create an interactive line plot of the closing prices for each symbol using Plotly
    st.subheader("Closing prices")
    fig = px.line(data,
                  x=data.index,
                  y='Close',
                  color='Symbol',
                  title='Closing Prices')
    st.plotly_chart(fig)

    # Calculate RSI for each symbol
    data['RSI'] = data.groupby('Symbol')['Close'].transform(
      lambda x: ta.momentum.RSIIndicator(x).rsi())

    total_earnings = 0
    buy_sell_signals = []
    summary_data = []

    buy_sell_counts = {}

    # Calculate earnings and buy/sell signals for each symbol
    for symbol in symbols_list:
      symbol_data = data[data['Symbol'] == symbol].copy()

      # Create Buy and Sell signals
      symbol_data['Buy'] = (symbol_data['RSI'] < rsi_min)
      symbol_data['Sell'] = (symbol_data['RSI'] > rsi_max)

      in_position = False
      buy_price = 0
      earnings = 0
      num_shares = 0

      buy_count = 0
      sell_count = 0

      # Initialize investment value for each ticker
      symbol_investment = total_investment / len(symbols_list)

      # on buy and sell signals
      for index, row in symbol_data.iterrows():
        if row['Buy'] and not in_position:
          in_position = True
          buy_price = row['Close']
          num_shares = symbol_investment // buy_price  # Calculate the number of shares to buy
          buy_amount = num_shares * buy_price
          buy_sell_signals.append({
            "Symbol": symbol,
            "Signal": "Buy",
            "Timestamp": index,
            "Price": buy_price,
            "Amount": buy_amount
          })
          buy_count += 1
        elif row['Sell'] and in_position:
          in_position = False
          sell_price = row['Close']
          earnings += num_shares * (
            sell_price - buy_price
          )  # Calculate earnings based on the number of shares
          sell_amount = num_shares * sell_price
          buy_sell_signals.append({
            "Symbol": symbol,
            "Signal": "Sell",
            "Timestamp": index,
            "Price": sell_price,
            "Amount": sell_amount,
            "Earnings": (sell_amount - buy_amount)
          })
          sell_count += 1

      buy_sell_counts[symbol] = {'Buy': buy_count, 'Sell': sell_count}

      # Update total earnings with the earnings from the current symbol
      total_earnings += earnings

      # Store the performance data of each ticker in summary_data list
      summary_data.append({
        "Symbol": symbol,
        "Earnings": earnings,
        "Investment": symbol_investment
      })

    # Calculate total returns based on the invested amount
    total_returns = total_investment + total_earnings

    # Create a bar chart for the number of buy and sell signals for each ticker
    st.subheader("Number of Buy and Sell Signals")
    buy_sell_counts_df = pd.DataFrame(buy_sell_counts).T.reset_index().rename(
      columns={'index': 'Symbol'})
    fig2 = px.bar(buy_sell_counts_df,
                  x='Symbol',
                  y=['Buy', 'Sell'],
                  barmode='group',
                  title='Number of Buy and Sell Signals')
    st.plotly_chart(fig2)

    # Create a pie chart showing the distribution of earnings among the tickers
    st.subheader("Earnings Distribution")
    earnings_data = pd.DataFrame(summary_data).set_index('Symbol')
    fig3 = px.pie(earnings_data,
                  values='Earnings',
                  names=earnings_data.index,
                  title='Earnings Distribution')
    st.plotly_chart(fig3)

    # Create a line chart showing the performance of each ticker
    st.subheader("Ticker Performance")
    performance_data = pd.DataFrame(summary_data).set_index('Symbol')
    performance_data['Investment'] = performance_data['Investment'].astype(
      float)
    performance_data['Returns'] = performance_data[
      'Earnings'] / performance_data['Investment'] * 100
    fig4 = px.line(performance_data,
                   y='Returns',
                   title='Performance of each Ticker')
    st.plotly_chart(fig4)

    # Display earnings and total returns in Streamlit metrics
    st.metric("Total Earnings", f"${total_earnings:.2f}")
    st.metric("Total Returns", f"${total_returns:.2f}")

    # Display a summary of all tickers' performance
    st.subheader("Summary of Performance")
    summary_df = pd.DataFrame(summary_data)
    summary_df['Investment'] = summary_df['Investment'].astype(float)
    summary_df[
      'Returns'] = summary_df['Earnings'] / summary_df['Investment'] * 100
    st.write(summary_df)

    signals_df = pd.DataFrame(buy_sell_signals)

    # Display a table with the list of buys and sells for each ticker
    st.subheader("List of Buy and Sell Orders")
    orders_data = []
    for symbol in symbols_list:
      symbol_orders = signals_df[signals_df['Symbol'] == symbol].copy()
      symbol_orders['Amount'] = symbol_orders['Amount'].astype(float)
      symbol_orders['Earnings'] = symbol_orders['Earnings'].astype(float)
      symbol_orders['Cumulative Amount'] = symbol_orders['Amount'].cumsum()
      symbol_orders['Cumulative Earnings'] = symbol_orders['Earnings'].cumsum()
      orders_data.append(symbol_orders)
    orders_df = pd.concat(orders_data)
    st.write(orders_df)

    # Display the investment amount for each ticker
    st.subheader("Investment Allocation")
    investment_data = pd.DataFrame(summary_data).set_index('Symbol')
    investment_data['Investment'] = investment_data['Investment'].astype(float)
    fig5 = px.pie(investment_data,
                  values='Investment',
                  names=investment_data.index,
                  title='Investment Allocation')
    st.plotly_chart(fig5)

    # Display a table with the number of buys and sells for each ticker
    st.subheader("Buy and Sell Counts")
    buy_sell_counts_df = pd.DataFrame(buy_sell_counts).T.reset_index().rename(
      columns={'index': 'Symbol'})
    st.write(buy_sell_counts_df)
