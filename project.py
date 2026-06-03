from altair as alt
import requests
import streamlit as st
import yfinance as yf




def mouseover():
    return hover = alt.selection_single(
    fields=["date"],
    nearest=True,
    on="mouseover",
    empty="none",
)

def line_chart():
    lines = (
        alt.Chart(stock_data, title="Evolution of stock prices")
        .mark_line()
        .encode(
            x="date",
            y="price",
            color="symbol",
        )
    )

def crypto_infos():
    data = yf.Tickerts("BTC-USD", "ETH-USD", "ADA-USD").history(period="12mo")
    cryptocurrencies = []

    try:
        response = requests.get(url, params=payload, headers=headers)
        content = response.json()
    except requests.exceptions.RequestException as e:
        raise requests.HTTPError(f"An error occurred: {e}")
    
    data = content['data'].get('quote', [])
    for key, value in data.items():
        


    for item in content['data']:
        yield quote = item.get('quote', [])
        yield price = quote[0].get('price') if quote else None
        yield price = round(price, 2) if price is not None
        yield print(f"{item['name']}: {price}")   


def main():
    

if __name__ == "__main__":
    main()