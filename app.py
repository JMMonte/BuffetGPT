import streamlit as st  # Import the streamlit library
import yfinance as yf
import pandas as pd
import ta  # Import the technical analysis library
import plotly.express as px
from datetime import datetime
from datetime import timedelta
from strategies import moving_average_strategy, momentum_strategy, bollinger_bands_strategy
import statsmodels.api as sm
from collections import OrderedDict
import re  # Import the regular expression library

st.set_page_config(page_title="Technical Analysis Backtester",
                   page_icon=None,
                   layout="wide",
                   initial_sidebar_state="expanded",
                   menu_items=None)

st.markdown(
    """
<style>
    button[kind="secondary"] {
        margin-bottom: 4rem!important;
    }
</style>
""",
    unsafe_allow_html=True,
)


INVESTMENT_STRATEGIES = OrderedDict([
    ("Moving Average Crossover", moving_average_strategy),
    ("Momentum", momentum_strategy),
    ("Bollinger Bands", bollinger_bands_strategy),
])


# Set the default answer status to False
answer_status = False

# Define the stock symbol validator


def is_valid_stock_symbol(symbol):
    return re.match(r"^[A-Za-z0-9\.\-\^]+$", symbol) is not None


# Time variables
now = datetime.now()
current_time = now.strftime("%H:%M:%S")
today = now.strftime("%d %B %Y")
time_ago = now - timedelta(days=120)

# Just a nice URL
url = ["https://www.investopedia.com/terms/r/rsi.asp", "https://www.investopedia.com/terms/b/bollingerbands.asp",
       "https://www.investopedia.com/terms/m/movingaverage.asp", "https://www.investopedia.com/terms/m/macd.asp", "https://github.com/JMMonte", "https://monte-negro.space"]

# Set the title of the app
st.title("Technical Analysis Backtester")

# Open the sidebar
with st.sidebar:
    # Input the total amount of money to be invested
    total_investment = st.number_input(
        "Enter the total amount of money to be invested:",
        min_value=0.0,
        value=10000.0,
        step=1.0)

    # Input the stock symbol and date range for backtesting
    symbol = st.text_input("Enter the Ticker symbol (e.g., AAPL, BTC-USD, VTI):",
                           "AAPL,NVDA,AMZN,TSLA", help="You can enter multiple stocks, ETFs, or Crypto by separating them with a comma.")
    try:
        if not symbol:
            raise ValueError
    except ValueError:
        st.error("Please enter an existing ticker that is listed in Yahoo Finance.")

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
        help="The RSI is a measure of the change in price over a period of time. A normal minimum value for a stock is 30 or less. For ETFs and index, use a value of 45 or 35."
    )
    # Set the max RSI value
    rsi_max = st.number_input(
        "Enter the maximum RSI value:",
        min_value=0.0,
        value=70.0,
        step=0.1,
        help="The RSI is a measure of the change in price over a period of time. A normal maximum value for a stock is 70 or more. For ETFs and index, use a value of 55 or 60."
    )

    strategy_name = st.selectbox("Select an investment strategy:",
                                 list(INVESTMENT_STRATEGIES.keys()))
    strategy_function = INVESTMENT_STRATEGIES[strategy_name]

    # Strategy specific inputs
    if strategy_name == "Moving Average Crossover":
        short_window = st.sidebar.number_input(
            "Short moving average window:",
            min_value=1,
            value=50,
            step=1,
            help="The number of days to calculate the short moving average."
        )
        long_window = st.sidebar.number_input(
            "Long moving average window:",
            min_value=1,
            value=200,
            step=1,
            help="The number of days to calculate the long moving average."
        )
        strategy_inputs = (short_window, long_window)
    elif strategy_name == "Momentum":
        momentum_window = st.sidebar.number_input(
            "Momentum window:",
            min_value=1,
            value=14,
            step=1,
            help="The number of days to calculate the momentum."
        )
        strategy_inputs = (momentum_window,)
    elif strategy_name == "Bollinger Bands":
        bollinger_window = st.sidebar.number_input(
            "Bollinger Bands window:",
            min_value=1,
            value=20,
            step=1,
            help="The number of days to calculate the Bollinger Bands."
        )
        bollinger_n_std = st.sidebar.number_input(
            "Bollinger Bands n standard deviations:",
            min_value=1.0,
            value=2.0,
            step=0.1,
            help="The number of standard deviations for the Bollinger Bands."
        )
        strategy_inputs = (bollinger_window, bollinger_n_std)

    # Fetch historical data using yfinance
    data = yf.download(symbol, start=start_date, end=end_date, interval="1d")

    # Create a "Backtest" button
    start_bot_button = st.button("Backtest")

    # Show the about section on the sidebar
    if answer_status:
        with st.expander("About this sandbox"):
            st.write(
                '''This is a simple backtesting sandbox that uses Yfinance history data to preform technical analysis, set a list of buy and sell orders and plot the resutl. It's pretty simple.
        For technical analysis, this bot uses RSI, or Relative Strength Index, which is a measure of the change in price over a period of time.
        More about RSI here: [Investopedia](%s).
        This bot was designed and built by [João Montenegro](%s), and you can find the source code on [GitHub](%s).
        ''' % (url[0], url[5], url[4]))

# Main backtesting section
if not start_bot_button:

    # Show a warning message if the bot is not running
    warning = st.warning(
        "👈 Your portfolio data will go here. Setup the bot in the side bar")

    # Show the about section on the main page
    st.write(
        '''This is a simple backtesting sandbox that uses Yfinance history data to preform technical analysis, set a list of buy and sell orders and plot the resutl. It's pretty simple.<br/>
      For technical analysis, this bot uses RSI, or Relative Strength Index, which is a measure of the change in price over a period of time.
      More about RSI here: [Investopedia](%s).<br/>
      This bot was designed and built by [João Montenegro](%s), and you can find the source code on [GitHub](%s).
      ''' % (url[0], url[5], url[4]), unsafe_allow_html=True)
    st.subheader("More about the available investment strategies:")
    cole1, cole2 = st.columns(2)
    container = st.container()

    st.subheader("Some ticker lists to get you started:")
    st.write('''
    Tech Stocks: 
    ```
    AAPL, NVDA, AMZN, TSLA
    ```

    '''

             )
    st.write('''
    ETFs: 
    ```
    SPY, QQQ, IWM, VOO
    ```

    '''

             )
    st.write('''
    Crypto: 
    ```
    BTC-USD, ETH-USD, DOGE-USD
    ```

    '''

             )
    st.write('''
    Forex: 
    ```
    EURUSD=X, GBPUSD=X, USDJPY=X
    ```

    '''

             )
    st.write('''
    Commodities: 
    ```
    GC=F, CL=F, SI=F
    ```

    '''

             )
    st.write('''
    Indices: 
    ```
    ^GSPC, ^IXIC, ^DJI, ^RUT
    ```

    '''

             )
    st.write('''
    Bonds: 
    ```
    ^TNX, ^IRX, ^TYX, ^FVX
    ```

    '''

             )
    st.write('''
    Currencies: 
    ```
    ^TNX, ^IRX, ^TYX, ^FVX
    ```

    '''

             )
    st.write('''
    Bruteforce: 
    ```
    AAPL, NVDA, AMZN, TSLA, SPY, QQQ, IWM, VOO, BTC-USD, ETH-USD, DOGE-USD, EURUSD=X, GBPUSD=X, USDJPY=X, GC=F, CL=F, SI=F, ^GSPC, ^IXIC, ^DJI, ^RUT, ^TNX, ^IRX, ^TYX, ^FVX
    ```

    '''

             )
    st.write('''
    Large ETF list: 
    ```
    QQQ, IVV, IWM, SPY, IJR, XLE, AGG, XLV, BND, IEMG, IEFA, EFA, XLK, GLD, VEA, VWO, VNQ, XLU, XLY, TLT, XLI, XLP, IEF, IGSB, GDX, IAU, XLF, GOVT, LQD, SHY, EEM, ACWI, VCSH, EMB, VCIT, JPST, BIL, JEPI, TQQQ, SQQQ, SH, TZA, SPXS, SOXS, SPXU, SDOW, VOO, PSQ, QID, BITO, XLB
    ```

    '''

             )

    # Explainers for the strategies
    with cole1:
        with st.expander("About Moving Average Crossover"):
            st.markdown("$Simple Moving Average = (A1 + A2 + …… + An) / n$<br/><br/>where:<br/><br/>$A_i$ is the data point in the i-th period.", unsafe_allow_html=True)
            st.write(
                "Moving Average Crossover is a strategy that uses two moving averages to determine when to buy and sell a stock. The strategy is based on the idea that a stock price will trend in a certain direction after it breaks above or below its moving average. The strategy is based on the idea that a stock price will trend in a certain direction after it breaks above or below its moving average. More about Moving Average Crossover here: [Investopedia](%s)" % url[2])
    with cole2:
        with st.expander("About Momentum Investing"):
            st.markdown("$Momentum = V − V_x$<br/><br/>where:<br/><br/>$V$ is the latest price<br/><br/>$V_x$ is the closing price $x$ number of days ago.", unsafe_allow_html=True)
            st.write(
                "Momentum investing is a strategy that aims to capitalize on the continuance of an existing market trend. It is a trading strategy in which investors buy securities that are already rising and look to sell them when they look to have peaked. Momentum, in markets, refers to the capacity for a price trend to sustain itself going forward. More about Moving Average Crossover here: [Investopedia](%s)" % url[2])
    with container:
        with st.expander("About Bollinger Bands"):
            st.markdown("$BOLU = MA(TP,n)+ m * σ[TP,n]$<br/>$BOLD = MA(TP,n) − m * σ[TP,n]$<br/><br/>where:<br/><br/>$BOLU$ = Upper Bollinger Band<br/><br/>$BOLD$ = Lower Bollinger Band<br/><br/>$MA$ = Moving average<br/><br/>$TP (typical price) = (High + Low + Close) ÷ 3$<br/><br/>$n$ = Number of days in smoothing period (typically 20)<br/><br/>$m$ = Number of standard deviations (typically 2)<br/><br/>$σ[TP,n]$ = Standard Deviation over last $n$ periods of $TP$ (Typical Price", unsafe_allow_html=True)
            st.write(
                "Bollinger Bands are a technical trading tool created by John Bollinger in the early 1980s. They are volatility bands placed above and below a moving average and are used to measure price volatility. Bollinger Bands can be used to identify high and low points in the market, as well as to identify overbought and oversold conditions. More about Moving Average Crossover here: [Investopedia](%s)" % url[1])


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
        answer_status = True
        col1, col2, col3 = st.columns(3, gap="large")

        # Create an interactive line plot of the closing prices for each symbol using Plotly
        st.subheader(
            "Closing prices of selected stocks, ETFs and/or indexes (USD)")
        fig = px.line(data,
                      x=data.index,
                      y='Close',
                      color='Symbol',
                      title='Closing Prices')
        st.plotly_chart(fig, use_container_width=True)

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

            # Apply the selected investment strategy
            try:
                strategy_function(symbol_data)
            except Exception as e:
                st.error(
                    f"Error applying strategy '{strategy_name}' to symbol '{symbol}': {e}")
                continue

            # Create Buy and Sell signals
            # symbol_data['Buy'] = (symbol_data['RSI'] < rsi_min)
            # symbol_data['Sell'] = (symbol_data['RSI'] > rsi_max)

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
                    # Calculate the number of shares to buy
                    num_shares = symbol_investment // buy_price
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

            # Store the number of buy and sell signals for each ticker
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
        st.plotly_chart(fig2, use_container_width=True)

        # Create a bar chart showing the performance of each ticker
        st.subheader("Ticker Performance")
        performance_data = pd.DataFrame(summary_data).set_index('Symbol')
        performance_data['Investment'] = performance_data['Investment'].astype(
            float)
        performance_data['Returns'] = performance_data[
            'Earnings'] / performance_data['Investment'] * 100
        fig4 = px.bar(performance_data,
                      y='Returns',
                      title='Performance of each Ticker')
        st.plotly_chart(fig4, use_container_width=True)

        # Display earnings and total returns in Streamlit metrics
        with col1:
            st.metric("Total Investment", "${:,.2f}".format(total_investment))
        with col2:
            st.metric("Total Earnings", "${:,.2f}".format(total_earnings))
        with col3:
            st.metric("Total Returns",
                      "${:,.2f}".format(total_returns),
                      delta=f"{total_earnings / total_investment * 100:.2f} %")

        cola1, cola2 = st.columns(2)
        with cola1:
            # Display a summary of all tickers' performance
            st.subheader("Summary of Performance")
            summary_df = pd.DataFrame(summary_data)
            summary_df['Investment'] = summary_df['Investment'].astype(float)
            summary_df[
                'Returns'] = summary_df['Earnings'] / summary_df['Investment'] * 100
            st.dataframe(summary_df, use_container_width=True)

            signals_df = pd.DataFrame(buy_sell_signals)

        with cola2:
            # Display a table with the number of buys and sells for each ticker
            st.subheader("Buy and Sell Counts")
            buy_sell_counts_df = pd.DataFrame(
                buy_sell_counts).T.reset_index().rename(columns={'index': 'Symbol'})
            st.dataframe(buy_sell_counts_df, use_container_width=True)

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
        st.dataframe(orders_df, use_container_width=True)

        # Initialize the starting treasury
        treasury = total_investment

        # Create a copy of the buy_sell_signals list
        buy_sell_list = buy_sell_signals.copy()

        # Insert a new dictionary at the beginning of the list to represent the starting treasury
        buy_sell_list.insert(
            0, {'Symbol': 'Treasury', 'Signal': 'Buy', 'Timestamp': start_date, 'Amount': treasury})

        # Sort the list by timestamp
        buy_sell_list_sorted = sorted(
            buy_sell_list, key=lambda x: x['Timestamp'])

        # Calculate the change in treasury for each timestamp
        for i in range(1, len(buy_sell_list_sorted)):
            signal = buy_sell_list_sorted[i]['Signal']
            amount = buy_sell_list_sorted[i]['Amount']
            if signal == 'Buy':
                treasury -= amount
            elif signal == 'Sell':
                treasury += amount
            buy_sell_list_sorted[i]['Amount'] = treasury

        # Convert the buy_sell_list_sorted to a Pandas DataFrame
        buy_sell_df = pd.DataFrame(buy_sell_list_sorted)

        # Plot the cumulative treasury using Plotly
        st.subheader("Cumulative treasury over time")
        fig_cumulative_treasury = px.scatter(buy_sell_df,
                                             x=buy_sell_df['Timestamp'],
                                             y=buy_sell_df['Amount'],
                                             title="Cumulative treasury over time",
                                             trendline="ols",
                                             trendline_scope="overall",
                                             trendline_color_override="red")
        st.plotly_chart(fig_cumulative_treasury.update_traces(
            mode='lines'), use_container_width=True)

        # Add a line graph showing buy and sell orders in time (timeframe)
        st.subheader("Buy and Sell Orders in Time")
        orders_data_graph = []
        for symbol in symbols_list:
            symbol_orders = signals_df[signals_df['Symbol'] == symbol].copy()
            symbol_orders['Amount'] = symbol_orders['Amount'].astype(float)
            orders_data_graph.append(symbol_orders)
        fig6 = px.line(pd.concat(orders_data_graph), x='Timestamp', y='Amount',
                       color='Symbol', title='Buy and Sell Orders in Time', markers=True)
        st.plotly_chart(fig6, use_container_width=True)

        coli1, coli2 = st.columns(2, gap="large")
        with coli1:
            # Create a pie chart showing the distribution of earnings among the tickers
            st.subheader("Earnings Distribution")
            earnings_data = pd.DataFrame(data=summary_data).set_index('Symbol')
            fig3 = px.pie(earnings_data,
                          values='Earnings',
                          names=earnings_data.index,
                          title='Earnings Distribution')
            st.plotly_chart(fig3, use_container_width=True)

        with coli2:
            # Display the investment amount for each ticker
            st.subheader("Investment Allocation")
            investment_data = pd.DataFrame(
                data=summary_data).set_index('Symbol')
            investment_data['Investment'] = investment_data['Investment'].astype(
                float)
            fig5 = px.pie(investment_data,
                          values='Investment',
                          names=investment_data.index,
                          title='Investment Allocation')
            st.plotly_chart(fig5, use_container_width=True)
