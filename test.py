import sqlite3

con = sqlite3.connect("finance.db")
cur = con.cursor()

cur.execute("ALTER TABLE assets ADD COLUMN asset_date DATE DEFAULT CURRENT_DATE;")
con.commit()
con.close()