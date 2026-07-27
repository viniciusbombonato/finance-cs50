import altair as alt
import bcrypt as bc
import json
import streamlit as st
import pandas as pd
import requests
import sqlite3
import yfinance as yf


class User_companies:
    def __init__(self, options_shares):
        self._options = []
        self._shares = []
        if self._options:
            for option, shares in options_shares.items():
                self._options.append(option)
                self._shares.append(shares)

        self.data = None
        self.user_assets = {}

    def fetch_company_tickers(self):
        try:
            with open("name_ticker.json", "r") as f:
                companies_tickers = []
                f = json.load(f)

                for name, ticker in f.items():
                    if name in self._options:
                        companies_tickers.append(ticker)
                
                return companies_tickers
        except Exception as e:
            return e
        
    def fetch_company_data(self, companies_tickers):
        try:
            self.data = yf.download(companies_tickers, period = "1d")
            self.data = self.data["Close"].iloc[-1]
            self.data = self.data.to_dict()
            return self.data
        except Exception as e:
            return e
    
    def data_to_store(self):

        #for witch ticker that the user own store in a dictionary that info
        index = 0
        for ticker, price in self.data.items():
            self.user_assets[ticker] = {"price": price, "amount": self._shares[index]}
            index = index + 1

        return self.user_assets

def main():
    user_tickers = ["TSLA", "AAPL", "MSFT", "GOOGL", "AMZN", "META"]

    user_tickers_price = User_companies(options_shares=[])
    user_tickers_price = user_tickers_price.fetch_company_data(user_tickers)

    for ticker, price in user_tickers_price.items():
        print(ticker)
        print(price)

if __name__ == "__main__":
    main()
