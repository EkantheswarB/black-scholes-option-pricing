# fetch_data.py

import yfinance as yf
import datetime

def get_stock_price(ticker):
    stock = yf.Ticker(ticker)
    data = stock.history(period="1d")
    if not data.empty:
        return data["Close"].iloc[-1]
    return None

def get_option_chain(ticker, expiry):
    stock = yf.Ticker(ticker)
    options = stock.option_chain(expiry)
    return options.calls, options.puts

def get_expiry_dates(ticker):
    stock = yf.Ticker(ticker)
    return stock.options

if __name__ == '__main__':
    ticker = "AAPL"
    expiry_list = get_expiry_dates(ticker)
    if expiry_list:
        latest_expiry = expiry_list[0]
        spot_price = get_stock_price(ticker)
        calls, puts = get_option_chain(ticker, latest_expiry)

        print(f"Ticker: {ticker}")
        print(f"Spot Price: {spot_price:.2f}")
        print(f"Expiry Date: {latest_expiry}")
        print("\nSample Call Options:")
        print(calls.head())
