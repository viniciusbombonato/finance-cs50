import streamlit as st
import pandas as pd
import yfinance as yf

tickers = ["BTC-USD", "ETH-USD", "BNB-USD", "SOL-USD"]
pd.set_option('display.max_rows', None) 


class CryptoData:
    def __init__(self, tickers):
        self.tickers = tickers
        self.data = None

    def fetch_data(self):
        try:
            self.data = yf.download(self.tickers, group_by="ticker", period="5d")
        except Exception as e:
            st.error(f"An error occurred while fetching cryptocurrency data: {e}", icon="🚨")
            self.data = None

    def process_data(self):
        if self.data is not None:
            try:
                self.data = self.data.melt(var_name="Symbol", value_name="Price", ignore_index=False).reset_index()
            except Exception as e:
                st.error(f"An error occurred while processing cryptocurrency data: {e}", icon="🚨")


crypto_data = CryptoData(tickers=tickers)
crypto_data.fetch_data()
crypto_data.process_data()
                
print(crypto_data.data)

