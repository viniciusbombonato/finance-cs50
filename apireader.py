import pandas as pd
import yfinance as yf

tickers = ["BTC-USD"]
data = yf.download(tickers)

# Reshape data: get Close prices for each ticker and stack into a long format
# prices = data['Close'].reset_index()
# tb = prices.melt(id_vars='Date', var_name='Ticker', value_name='Price')
print(data)