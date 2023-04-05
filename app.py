from datetime import date, timedelta
import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd

from utils.data_fetcher import fetch_data
from utils.visualizations import calculate_portfolio_value
from utils.portfolio_manager import PortfolioManager
from utils.risk_management import RiskManagement

from strategies.momentum_investing import MomentumInvesting
from strategies.mean_reversion import MeanReversion
from strategies.passive_investing import PassiveInvesting

st.set_page_config(layout="wide")

today = date.today()
history_in_days = 365 * 10
history_date = today - timedelta(days=history_in_days)

def validate_ticker_input(ticker_input):
    ticker_list = [ticker.strip() for ticker in ticker_input.split(",")]

    if len(ticker_list) == 0 or ticker_list == ['']:
        st.error("Please enter at least one ticker.")
        return None

    return ticker_list

def run_bot(strategy, data, investment_amount, investment_cycle, start_date, end_date, rebalance_frequency='M'):
    investment_log = []
    current_date = start_date
    rebalance_date = pd.to_datetime(current_date).to_period(rebalance_frequency).to_timestamp()

    while current_date <= end_date and st.session_state.running:
        try:
            strategy.analyze()
            orders = strategy.execute()

            investment_log.append({
                'date': current_date,
                'orders': orders
            })

            # Display the current status of the bot in the UI
            status = f"Date: {current_date.strftime('%Y-%m-%d')}, Orders: {orders}"
            st.write(status)

            if current_date >= pd.Timestamp(rebalance_date):

                portfolio_manager.rebalance(strategy="equal_weight")
                rebalance_date += pd.to_timedelta(pd.offsets.MonthEnd())

            current_date += pd.to_timedelta(investment_cycle, unit='m')

        except Exception as e:
            st.error(f"An error occurred while running the bot: {str(e)}")
            st.session_state.running = False

    return investment_log

# Start the UI
st.title("BuffetGPT - Automated Investment Bot")

# UI columns
col1, col2 = st.columns([1,2])

# Left side of the UI
with col1:
    investment_amount = st.number_input("Enter the amount you want to invest ($):", min_value=0.0, step=0.1, value=1000.0, help="The amount of money you want to invest in the backtest.")
    strategies = ["Momentum Investing", "Mean Reversion", "Passive Investing"]
    selected_strategies = st.multiselect("Select investment strategies:", strategies, default=strategies[0])

    stop_loss = st.number_input("Enter the stop loss percentage:", min_value=0.0, step=0.1, value=5.0, help="The maximum allowable loss for a single stock position, as a percentage of its entry price.")
    take_profit = st.number_input("Enter the take profit percentage:", min_value=0.0, step=0.1, value=10.0, help="The desired profit target for a single stock position, as a percentage of its entry price.")

    start_date = st.date_input("Choose the start date for the backtest:", history_date)
    end_date = st.date_input("Choose the end date for the backtest (optional):", today)

    ticker_input = st.text_input("Enter the tickers to include in the backtest (comma-separated):", placeholder="AAPL,MSFT,AMZN", help="The tickers of the stocks you want to include in the backtest. Separate each ticker with a comma.")
    ticker_list = validate_ticker_input(ticker_input)


    investment_cycle = st.number_input("Select investment cycle (in minutes):",min_value=1.0, step=0.1,max_value=1500.0, help="The cycle that the bot will run in minutes")

    if 'running' not in st.session_state:
        st.session_state.running = False

    run_state = st.empty()

    with st.form(key='investment_form'):
        col_bt1, col_bt2 = st.columns(2)
        with col_bt1:
            run_state = st.form_submit_button(label='Run')
        with col_bt2:
            stop_state = st.form_submit_button(label='Stop')

with col2:
    st.subheader("Bot Status:")
    
    if run_state and not st.session_state.running:
        st.session_state.running = True

        if ticker_list == ['']:
            st.error("Please enter at least one ticker.")
            st.session_state.running = False
        else:
            data = fetch_data(ticker_list, start_date, end_date)

            strategies = {
                "Momentum Investing": MomentumInvesting(data, investment_amount, int(investment_cycle)),
                "Mean Reversion": MeanReversion(data, investment_amount, int(investment_cycle)),
                "Passive Investing": PassiveInvesting(data, investment_amount, int(investment_cycle)),
            }

            portfolio_manager = PortfolioManager()
            risk_management = RiskManagement(stop_loss,take_profit)

            for strategy_name in selected_strategies:
                strategy = strategies[strategy_name]
                investment_log = run_bot(strategy, data, investment_amount, int(investment_cycle), start_date, end_date)
                investment_log = risk_management.apply_stop_loss(investment_log, data)
                adjusted_investment_log = risk_management.apply_take_profit(investment_log, data)


                # Display the adjusted investment log generated by the bot
                st.write(f"{strategy_name} Adjusted Investment Log:")
                st.write(adjusted_investment_log)



                # Calculate and plot the portfolio value
                portfolio_value = calculate_portfolio_value(adjusted_investment_log, data)
                if portfolio_value:
                    dates, values = zip(*portfolio_value)
                plt.plot(dates, values)
                plt.xlabel('Date')
                plt.ylabel('Portfolio Value ($)')
                plt.title(f'{strategy_name} Investment Performance')
                st.pyplot(plt)

            st.session_state.running = False

    if stop_state and st.session_state.running:
        st.session_state.running = False
        st.write("Bot stopped.")

if st.session_state.running:
    investment_log = run_bot(MomentumInvesting, data, investment_amount, int(investment_cycle), start_date, end_date)

    # Display the investment log generated by the bot
    st.write("Momentum Investing Investment Log:")
    st.write(investment_log)
    st.session_state.running = False

