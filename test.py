import sqlite3

with sqlite3.connect("finance.db") as con:
    cur = con.cursor()

    cur.execute("SELECT asset_ticker, average_price FROM assets WHERE user_id = 2")
    res = cur.fetchall()

    
print(res)