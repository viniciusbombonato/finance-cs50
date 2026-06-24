import altair as alt
import pandas as pd
import requests
import newsapi
import streamlit as st
import yfinance as yf

cryptocoins = ["ETH-USD", "BNB-USD", "SOL-USD"]
companies = ["TSLA", "AAPL", "MSFT", "GOOGL", "AMZN", "META"]

st.set_page_config(
    page_title="Finance Information",
    page_icon="💹",
    layout="wide",
)

class Finance_data:
    def __init__(self, tickers):
        self.tickers = tickers
        self.data = None

    def fetch_data(self):
        try:
            self.data = yf.download(self.tickers, group_by="ticker")
        except Exception as e:
            st.error(f"An error occurred while fetching market data: {e}", icon="🚨")
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

def make_chart(data, title="Evolution of prices"):
    if data is None or data.empty:
        st.warning("No data available to display.")
        return
    
    hover = alt.selection_single(
    fields=["Date"],
    nearest=True,
    on="mouseover",
    empty="none",
    )

    lines = (
        alt.Chart(data, title=title)
        .mark_line()
        .encode(
            x="Date:T",
            y="Price:Q",
            color="Symbol:N",
        )
    )

    points = lines.transform_filter(hover).mark_circle(size=65)

    tooltips = (
        alt.Chart(data)
        .mark_rule()
        .encode(
            x="Date:T",
            y="Price:Q",
            opacity=alt.condition(hover, alt.value(0.3), alt.value(0)),
            tooltip=[
                alt.Tooltip("Date", title="Date"),
                alt.Tooltip("Price", title="Price (USD)"),
            ],
        )
        .add_selection(hover)
    )

    data_layer = (lines + points + tooltips).resolve_scale(y="shared")
    st.altair_chart(data_layer, use_container_width=True)

def what_new():
    st.markdown("## Latest News", text_alignment="center")
    try:
        response = requests.get(
            "https://newsapi.org/v2/top-headlines?country=us&apiKey=3a1bc10b310d450da381e508babd0df7"
        )
        if response.status_code != 200:
            st.error(f"News API request failed with status code: {response.status_code}")
            return

        response = response.json()
        articles = response.get("articles", [])

    except Exception as e:
        st.error(f"An error occurred while fetching news data: {e}", icon="🚨")
        return

    if not articles:
        st.info("No news articles available right now.")
        return

    col1, col2 = st.columns(spec=2, gap="large")

    for index, article in enumerate(articles):
        if index % 2 == 0:
            with col1:
                st.markdown("### " + article.get("title", "Untitled"))
                image_url = article.get("urlToImage")
                if image_url:
                    st.image(image=image_url, width="stretch")
                st.write(article.get("description", "No description available."))
        else:
            with col2:
                st.markdown("### " + article.get("title", "Untitled"))
                image_url = article.get("urlToImage")
                if image_url:
                    st.image(image=image_url, width="stretch")
                st.write(article.get("description", "No description available."))

def page_2():
    st.title("Dashboard")

pg = st.navigation(["dashboard.py", page_2])


def main():
    crypto_data = Finance_data(cryptocoins)
    crypto_data.fetch_data()
    crypto_data = crypto_data.process_data()
    make_chart(crypto_data, title="Evolution of Cryptocurrency Prices")

    company_data = Finance_data(companies)
    company_data.fetch_data()
    company_data = company_data.process_data()
    make_chart(company_data, title="Evolution of Company Prices")

    what_new()


if __name__ == "__main__":
    main()