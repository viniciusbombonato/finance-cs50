# import json
# import yfinance as yf

# class User_companies:
#     def __init__(self, options_shares):
#         self._options = []
#         self._shares = []
#         for option, shares in options_shares.items():
#             self._options.append(option)
#             self._shares.append(shares)


#         self.options = self._options
#         self.data = None
#         self.amount = self._shares
#         self.user_assets = {}
    
#     def fetch_company_tickers(self):
#         try:
#             with open("company_tickers.json", "r") as f:
#                 companies_tickers = []
#                 f = json.load(f)

#                 for value in f.values():
#                     if value["ticker"] in self.options:
#                         companies_tickers.append(value["ticker"])
                
#                 return companies_tickers
#         except Exception as e:
#             return e
        
#     def fetch_company_data(self, companies_tickers):
#         try:
#             self.data = yf.download(companies_tickers, period = "1d")
#             self.data = self.data["Close"].iloc[-1]
#             return self.data.to_dict()
#         except Exception as e:
#             return e
    
#     def data_to_store(self):

#         #for witch ticker that the user own store in a dictionary that info
#         index = 0
#         for ticker, price in self.data.items():
#             self.user_assets[ticker] = {"price": price, "amount": self.amount[index]}
#             index = index + 1

#         return self.user_assets
    


import sqlite3

con = sqlite3.connect("finance.db")
cur = con.cursor()

cur.execute("ALTER TABLE assets DROP COLUMN COLLUMN")
con.commit()
con.close()
