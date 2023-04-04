import pandas as pd

class PortfolioManager:
    def __init__(self):
        self.portfolio = pd.DataFrame(columns=['ticker', 'shares', 'purchase_price'])

    def execute_orders(self, orders):
        for order in orders:
            ticker = order['ticker']
            shares = order['shares']
            price = order['price']

            # Check if the ticker already exists in the portfolio
            if ticker in self.portfolio['ticker'].values:
                # Update the existing position
                index = self.portfolio[self.portfolio['ticker'] == ticker].index[0]
                self.portfolio.at[index, 'shares'] += shares
                self.portfolio.at[index, 'purchase_price'] = price
            else:
                # Add a new position to the portfolio
                self.portfolio = self.portfolio.append({
                    'ticker': ticker,
                    'shares': shares,
                    'purchase_price': price
                }, ignore_index=True)

    def calculate_portfolio_value(self, data):
        total_value = 0

        for _, position in self.portfolio.iterrows():
            ticker = position['ticker']
            shares = position['shares']
            latest_price = data[ticker]['Close'].iloc[-1]
            total_value += shares * latest_price

        return total_value
    
    def update_portfolio(self, data):
        updated_portfolio = self.portfolio.copy()

        for index, position in self.portfolio.iterrows():
            ticker = position['ticker']
            latest_price = data[ticker]['Close'].iloc[-1]
            updated_portfolio.at[index, 'current_price'] = latest_price

            # Calculate profit/loss for each position
            purchase_price = position['purchase_price']
            shares = position['shares']
            updated_portfolio.at[index, 'profit_loss'] = (latest_price - purchase_price) * shares

        return updated_portfolio

