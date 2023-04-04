import pandas as pd
import streamlit as st
from strategies.strategy_base import StrategyBase

class PassiveInvesting(StrategyBase):
    def __init__(self, data, investment_amount, invest_cycle):
        self.data = data
        self.investment_amount = investment_amount
        self.invest_cycle = invest_cycle

    def analyze(self):
        self.candidates = {ticker: self.data[ticker]['Close'].iloc[-1] for ticker in self.data.keys()}

    def execute(self):
        available_funds = self.investment_amount
        investment_per_stock = available_funds / len(self.candidates)

        orders = []
        for ticker, current_price in self.candidates.items():
            num_shares = int(investment_per_stock / current_price)

            order = {
                'ticker': ticker,
                'price': current_price,
                'shares': num_shares,
                'type': 'buy'
            }
            orders.append(order)
            available_funds -= num_shares * current_price

        return orders
