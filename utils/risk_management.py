class RiskManagement:
    def __init__(self, stop_loss, take_profit):
        self.stop_loss = stop_loss
        self.take_profit = take_profit

    def apply_stop_loss(self, investment_log, data):
        adjusted_investment_log = []

        for entry in investment_log:
            orders = entry['orders']
            adjusted_orders = []

            for order in orders:
                ticker = order['ticker']
                entry_price = order['price']

                stop_loss_price = entry_price * (1 - self.stop_loss / 100)

                adjusted_order = order.copy()
                adjusted_order['stop_loss'] = stop_loss_price
                adjusted_orders.append(adjusted_order)

            adjusted_entry = entry.copy()
            adjusted_entry['orders'] = adjusted_orders
            adjusted_investment_log.append(adjusted_entry)

        return adjusted_investment_log

    def apply_take_profit(self, investment_log, data):
        adjusted_investment_log = []

        for entry in investment_log:
            orders = entry['orders']
            adjusted_orders = []

            for order in orders:
                ticker = order['ticker']
                entry_price = order['price']

                take_profit_price = entry_price * (1 + self.take_profit / 100)

                adjusted_order = order.copy()
                adjusted_order['take_profit'] = take_profit_price
                adjusted_orders.append(adjusted_order)

            adjusted_entry = entry.copy()
            adjusted_entry['orders'] = adjusted_orders
            adjusted_investment_log.append(adjusted_entry)

        return adjusted_investment_log