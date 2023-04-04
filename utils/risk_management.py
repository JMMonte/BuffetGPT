class RiskManagement:
    def __init__(self, max_position_size, min_position_size, max_portfolio_exposure, stop_loss, take_profit):
        self.max_position_size = max_position_size
        self.min_position_size = min_position_size
        self.max_portfolio_exposure = max_portfolio_exposure
        self.stop_loss = stop_loss
        self.take_profit = take_profit

    def adjust_orders(self, orders, portfolio_value):
        adjusted_orders = []
        for order in orders:
            ticker, action, quantity, price = order

            # Adjust the order based on the max_position_size
            position_size = quantity * price
            max_position_value = self.max_position_size * portfolio_value
            if position_size > max_position_value:
                new_quantity = int(max_position_value / price)
                if new_quantity == 0:
                    continue
                order = (ticker, action, new_quantity, price)

            # Adjust the order based on the min_position_size
            min_position_value = self.min_position_size * portfolio_value
            if position_size < min_position_value:
                new_quantity = int(min_position_value / price)
                order = (ticker, action, new_quantity, price)

            adjusted_orders.append(order)
        return adjusted_orders

    def apply_stop_loss_and_take_profit(self, investment_log, data):
        adjusted_investment_log = []
        for entry in investment_log:
            date, orders = entry['date'], entry['orders']
            adjusted_orders = []

            for order in orders:
                ticker, action, quantity, price = order

                # Apply stop loss and take profit only for sell orders
                if action == 'SELL':
                    initial_price = None
                    for past_entry in investment_log:
                        for past_order in past_entry['orders']:
                            if past_order[0] == ticker and past_order[1] == 'BUY':
                                initial_price = past_order[3]
                                break
                        if initial_price:
                            break

                    if initial_price:
                        loss = (price - initial_price) / initial_price
                        if loss <= -self.stop_loss:
                            adjusted_orders.append(order)
                        elif loss >= self.take_profit:
                            adjusted_orders.append(order)
                    else:
                        adjusted_orders.append(order)
                else:
                    adjusted_orders.append(order)

            adjusted_investment_log.append({'date': date, 'orders': adjusted_orders})

        return adjusted_investment_log
