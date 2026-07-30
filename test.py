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
        self._options = list(options_shares.keys())
        self._shares = list(options_shares.values())

        self.data = None
        self.user_assets = {}

    def fetch_company_tickers(self):
        try:
            companies_tickers = []
            with open("name_ticker.json", "r") as f:
                companies_tickers = []
                f = json.load(f)

                for name, ticker in f.items():
                    if name in self._options:
                        companies_tickers.append(ticker)
                
            return companies_tickers
            
        except FileNotFoundError as e:
            raise FileNotFoundError("The filfe \" name_ticker.json\" was not found") from e
        except json.JSONDecodeError as e:
            raise ValueError("Error while trying to decode json file, check the format") from e
        except (AttributeError, KeyError) as e:
            raise ValueError("Not a Dictionarie, check the format") from e
        except Exception as e:
            raise ValueError("An error occur") from e
             
        
    def fetch_company_data(self, companies_tickers):
        try:
            self.data = yf.download(companies_tickers, period = "1d")
            self.data = self.data["Close"].iloc[-1]
            self.data = self.data.to_dict()

            return self.data
        
        except RuntimeError as e:
            raise RuntimeError("Error on yfinance API")  from e
        except (ValueError, AttributeError) as e:
            raise ValueError(f"Could not fomart the data, check if it is indeed a dictionarie: {e}") from e
        except Exception as e:
            raise ValueError("An error occur") from e
    
    def data_to_store(self):

        #for witch ticker that the user own store in a dictionary that info
        index = 0
        for ticker, price in self.data.items():
            self.user_assets[ticker] = {"price": price, "amount": self._shares[index]}
            index = index + 1

        return self.user_assets

def main():
    user_tickers = ["TSLA", "AAPL", "MSFT", "GOOGL", "AMZN", "META"]
    options_shares = {"MICROSOFT CORP": 12, "Meta Platforms, Inc.": 2, "VISA INC.": 90}

    user_tickers = User_companies(options_shares=options_shares)
    user_tickers = user_tickers.fetch_company_tickers()

    print(user_tickers)

    # for ticker, price in user_tickers_price.items():
    #     print(ticker)
    #     print(price)

if __name__ == "__main__":
    main()
