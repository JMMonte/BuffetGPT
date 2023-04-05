from strategies.strategy_base import StrategyBase

class MeanReversion(StrategyBase):
    def __init__(self, data, investment_amount, invest_cycle):
        self.data = data
        self.investment_amount = investment_amount
        self.invest_cycle = invest_cycle

    def analyze(self):
        moving_average_period = 50  # Customize the period for the moving average calculation
        candidates = {}

        for ticker, historical_data in self.data.items():
            historical_data['MovingAverage'] = historical_data['Close'].rolling(window=moving_average_period).mean()
            current_price = historical_data['Close'].iloc[-1]
            moving_average = historical_data['MovingAverage'].iloc[-1]

            if current_price < moving_average:
                candidates[ticker] = current_price

        self.candidates = candidates

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
