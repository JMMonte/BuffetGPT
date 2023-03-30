import schedule
import time
from investment_bot import InvestmentBot

def run_investment_bot():
    investment_bot = InvestmentBot()
    investment_bot.run_strategy()
    print("Investment strategy executed.")

def setup_scheduler(interval="weekly"):
    if interval == "weekly":
       schedule.every(7).days.at("00:00").do(run_investment_bot) # run weekly at midnight
    elif interval == "daily":
        schedule.every().day.at("00:00").do(run_investment_bot) # run daily at midnight
    # Add more scheduling options if needed

    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    setup_scheduler()
