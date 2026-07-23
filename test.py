import yfinance as yf
import pandas as pd
import streamlit as st

companies = ["TSLA", "AAPL", "MSFT", "GOOGL", "AMZN", "META"]

class Finance_data:
    def __init__(self, tickers):
        self.tickers = tickers
        self.data = None

    def fetch_data(self):
        try:
            self.data = yf.download(self.tickers, group_by="ticker")
        except Exception as e:
            st.error(f"An error occurred while fetching market data: {e}", icon="🚨")
            self.data = None

    def process_data(self):
        if self.data is not None:
            try:
                df_close = self.data.xs("Close", level=1, axis=1)
                self.data = df_close.melt(var_name="Symbol", value_name="Price", ignore_index=False).reset_index()
                self.data["Date"] = pd.to_datetime(self.data["Date"])
                self.data["Price"] = self.data["Price"].round(2)

                self.data = pd.DataFrame(self.data)
                return self.data
                
            except Exception as e:
                st.error(f"An error occurred while processing cryptocurrency data: {e}", icon="🚨")


test = Finance_data(companies)
test.fetch_data()
result = test.process_data()
print(result)
