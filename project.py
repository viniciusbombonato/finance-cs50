import altair as alt
import streamlit as st
import yfinance as yf

tickers = ["BTC-USD", "ETH-USD", "BNB-USD", "RP-USD", "SOL-USD"]
data = yf.download(tickers)


def mouseover():
    hover = alt.selection_single(
    fields=["date"],
    nearest=True,
    on="mouseover",
    empty="none",
)

def line_chart():
    lines = (
        alt.Chart(data, title="Evolution of Cryptocurrency prices")
        .mark_line()
        .encode(
            x="Date",
            y="Price",
            color="Symbol",
        )
    )

def crypto_infos():
    tickers = ["BTC-USD", "ETH-USD", "BNB-USD", "RP-USD", "SOL-USD"]
    try:
        data = yf.download(tickers)
    except Exception as e:
        st.error(f"An error occurred while fetching cryptocurrency data: {e}", icon="🚨")
        return

    cryptocurrencies = []

    for key, value in data.items():
        


    for item in content['data']:
        yield quote = item.get('quote', [])
        yield price = quote[0].get('price') if quote else None
        yield price = round(price, 2) if price is not None
        yield print(f"{item['name']}: {price}")   


def main():
    

if __name__ == "__main__":
    main()