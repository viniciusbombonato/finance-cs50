# import sqlite3

# con = sqlite3.connect("finance.db")
# cur = con.cursor()

# cur.execute("ALTER TABLE assets ADD COLUMN asset_date DATE DEFAULT CURRENT_DATE;")
# con.commit()
# con.close()

import pandas as pd
import yfinance as yf

tickers = ["TSLA"]

data = yf.download(tickers, period = "1d")
# data = pd.DataFrame(data)

print(data["Close"] * 10)