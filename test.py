import sqlite3

with sqlite3.connect("finance.db") as con:
        cur = con.cursor()

        cur.execute("SELECT  FROM assets WHERE user_id = 2")
        res = cur.fetchone()
        if res:
            print(res)
        
            