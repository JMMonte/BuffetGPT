# Technical Analysis Backtester

This is a technical analysis backtesting app that allows you to test different investment strategies on historical stock, ETF or cryptocurrency price data. The app uses the yfinance library to fetch historical data from Yahoo Finance, and the ta library to perform technical analysis. You can input the total amount of money to be invested, the stock symbol(s), the date range for backtesting, and the minimum and maximum RSI values. The app then calculates the buy and sell signals based on the chosen investment strategy (Moving Average Crossover, Momentum, or Bollinger Bands).

The app then calculates the performance of each symbol, including the number of buy and sell signals, and displays the results in various charts and tables. These include line plots of the closing prices, bar charts of buy and sell signals, and pie charts of earnings distribution and investment allocation. The app also displays the cumulative treasury over time and the buy and sell orders in time.

You can use this app to test different investment strategies on historical data to help you make informed decisions when investing in stocks, ETFs, or cryptocurrencies.

## Installation

To install the required libraries, run the following command:

```!/bin/bash
pip install streamlit yfinance pandas ta plotly statsmodels
```

## Usage

1. Run the app using Streamlit: `streamlit run app.py`

2. Open the app in your web browser at <http://localhost:8501>.

3. Input the required parameters (total investment, stock symbol(s), date range, and RSI values) in the sidebar.

4. Select an investment strategy (Moving Average Crossover, Momentum, or Bollinger Bands) from the dropdown menu.

5. Click the "Start Bot" button to start the backtesting process.

6. Analyze the results displayed in the various charts and tables.

## Features

- Fetch historical stock, ETF or cryptocurrency price data from Yahoo Finance
- Perform technical analysis using the ta library
- Calculate buy and sell signals based on chosen investment strategy
- Visualize results in various charts and tables
- Display cumulative treasury over time and buy and sell orders in time
- Analyze the performance of each symbol, including the number of buy and sell signals, earnings distribution, and investment allocation

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)
