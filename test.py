import altair as alt
import bcrypt as bc
import json
import streamlit as st
import pandas as pd
import requests
import sqlite3
import yfinance as yf


with sqlite3.connect("finance.db") as con:
        cur = con.cursor()

        cur.execute("SELECT asset_ticker, average_price FROM assets WHERE user_id = 3")
        res = cur.fetchall()
        if res:
            print(res)
        else:
            print(1)
