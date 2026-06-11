import altair as alt
import pandas as pd
import streamlit as st
import yfinance as yf

tickers = ["BTC-USD", "ETH-USD", "BNB-USD", "RP-USD", "SOL-USD"]

class CryptoData:
    def __init__(self, tickers):
        self.tickers = tickers
        self.data = None

    def fetch_data(self):
        try:
            self.data = yf.download(self.tickers, group_by="ticker")
        except Exception as e:
            st.error(f"An error occurred while fetching cryptocurrency data: {e}", icon="🚨")
            self.data = None

    def process_data(self):
        if self.data is not None:
            try:
                df_close = self.data.xs("Close", level=1, axis=1)
                self.data = df_close.melt(var_name="Symbol", value_name="Price", ignore_index=False).reset_index()
                self.data["Date"] = pd.to_datetime(self.data["Date"])
                self.data["Price"] = self.data["Price"].round(2)

                self.data = pd.DataFrame(self.data)
                return self.data
                
            except Exception as e:
                st.error(f"An error occurred while processing cryptocurrency data: {e}", icon="🚨")
        


def make_chart(crypto_data):

    if crypto_data is None or crypto_data.empty:
        st.warning("No cryptocurrency data available to display.")
        return

    hover = alt.selection_single(
    fields=["Date"],
    nearest=True,
    on="mouseover",
    empty="none",
    )
    
    lines = (
        alt.Chart(crypto_data, title="Evolution of Cryptocurrency prices")
        .mark_line()
        .encode(
            x="Date:T",
            y="Price:Q",
            color="Symbol:N",
        )
    )


    points = lines.transform_filter(hover).mark_circle(size=65)

    tooltips = (
        alt.Chart(crypto_data)
        .mark_rule()
        .encode(
            x="yearmonthdate(Date)",
            y="Price",
            opacity=alt.condition(hover, alt.value(0.3), alt.value(0)),
            tooltip=[
                alt.Tooltip("Date", title="Date"),
                alt.Tooltip("Price", title="Price (USD)"),
            ],
        )
        .add_selection(hover)
    )

    data_layer = (lines + points + tooltips).resolve_scale(y="independent")
    
    st.altair_chart(data_layer, use_container_width=True)


def main():
    crypto_data = CryptoData(tickers)
    crypto_data.fetch_data()
    crypto_data = crypto_data.process_data()

    make_chart(crypto_data)


if __name__ == "__main__":
    main()