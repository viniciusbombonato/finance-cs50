import sqlite3

con = sqlite3.connect("login.db")
cur = con.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS users (username, password)")