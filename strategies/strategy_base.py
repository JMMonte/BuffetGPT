class StrategyBase:
    def __init__(self, data, investment_amount, investment_cycle):
        self.data = data
        self.investment_amount = investment_amount
        self.investment_cycle = investment_cycle

    def analyze(self):
        raise NotImplementedError

    def execute(self):
        raise NotImplementedError
