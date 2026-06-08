import altair as alt
import streamlit as st
import yfinance as yf

tickers = ["BTC-USD", "ETH-USD", "BNB-USD", "RP-USD", "SOL-USD"]

class CryptoData:
    def __init__(self, tickers):
        self.tickers = tickers
        self.data = None

    def fetch_data(self):
        try:
            self.data = yf.download(self.tickers)
        except Exception as e:
            st.error(f"An error occurred while fetching cryptocurrency data: {e}", icon="🚨")
            self.data = None

    def process_data(self):
        


def make_chart(crypto_data):

    hover = alt.selection_single(
    fields=["date"],
    nearest=True,
    on="mouseover",
    empty="none",
)
    
    lines = (
        alt.Chart(crypto_data.data, title="Evolution of Cryptocurrency prices")
        .mark_line()
        .encode(
            x="Date",
            y="Price",
            color="Symbol",
        )
    )


    points = lines.transform_filter(hover).mark_circle(size=65)

    tooltips = (
        alt.Chart(crypto_data.data)
        .mark_rule()
        .encode(
            x="yearmonthdate(date)",
            y="price",
            opacity=alt.condition(hover, alt.value(0.3), alt.value(0)),
            tooltip=[
                alt.Tooltip("date", title="Date"),
                alt.Tooltip("price", title="Price (USD)"),
            ],
        )
        .add_selection(hover)
    )

    data_layer = lines + points + tooltips
    
    st.altair_chart(data_layer, use_container_width=True)


def main():
    crypto_data = CryptoData(tickers)

    crypto_chart = make_chart(crypto_data)


if __name__ == "__main__":
    main()