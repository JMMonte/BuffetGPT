# BuffetGPT streamlit investment bot

This is a streamlit app that uses BuffetGPT to generate investment strategies, backtest them, and evaluate their performance.

## Installation

1. Clone the repository
2. Run `pip install -r requirements.txt`

## Usage

1. On your terminal, go to the directory where you cloned the repository.
2. Run `streamlit run app.py`.
3. A streamlit app will open in your browser.

## Mechanisms

### Investment strategy

The bot follows a combination of the following strategies:

- Momentum Investing
- Passive investing
- Mean reversion

### Investment machine

1. get historic max data of stocks until today and store them.
2. get current price of each ticker
3. preform analysis on the history of each ticker and evaluate each ticker with an “interest” value. following the investment strategies selected by user.
4. decide wether to buy or not. this will be based on calculating wether there is still money available to invest, and the current interest of each ticker. Each cycle will end with an investment plan: which tickers to invest,how much, and when.
5. Each investment plan will be logged to compare preformance.
6. Preform steps 2-5 every investment cycle (measured in minutes)
7. the visualization of the performance will use the latest data in the investment plan.

### Not to be confused with the BuffetGPT GPT-2 model

BuffetGPT is a GPT-2 model trained on Warren Buffett's letters to shareholders. It is available on [Hugging Face](https://huggingface.co/lewtun/buffetgpt).
