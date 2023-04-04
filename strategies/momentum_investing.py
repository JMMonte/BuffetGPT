import pandas as pd
import streamlit as st
from strategies.strategy_base import StrategyBase

class MomentumInvesting(StrategyBase):
    def __init__(self, data, investment_amount, invest_cycle):
        self.data = data
        self.investment_amount = investment_amount
        self.invest_cycle = invest_cycle

    def analyze(self):
        momentum_scores = {}
        for ticker, historical_data in self.data.items():
            if len(historical_data) > self.invest_cycle:
                historical_data['Momentum'] = historical_data['Close'].pct_change(self.invest_cycle)
                momentum_scores[ticker] = historical_data['Momentum'].iloc[-1]
            else:
                st.error(f"Not enough data for {ticker} to calculate momentum. Skipping this stock.")
        self.rankings = pd.Series(momentum_scores).sort_values(ascending=False)
        self.current_prices = {ticker: self.data[ticker]['Close'].iloc[-1] for ticker in self.rankings.index}
        
    def execute(self):
        top_n = 3  # The number of top stocks to invest in
        available_funds = self.investment_amount
        investment_per_stock = available_funds / top_n

        orders = []
        for i, (ticker, momentum_score) in enumerate(self.rankings.head(top_n).iteritems()):
            stock_price = self.current_prices[ticker]
            num_shares = int(investment_per_stock / stock_price)

            order = {
                'ticker': ticker,
                'price': stock_price,
                'shares': num_shares,
                'type': 'buy'
            }
            orders.append(order)
            available_funds -= num_shares * stock_price

        return orders

