import altair as alt
import pandas as pd
import requests
import streamlit as st
from streamlit_option_menu import option_menu
import yfinance as yf

cryptocoins = ["ETH-USD", "BNB-USD", "SOL-USD"]
companies = ["TSLA", "AAPL", "MSFT", "GOOGL", "AMZN", "META"]

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
    try:
        response = requests.get(
            "https://newsapi.org/v2/top-headlines?country=us&apiKey=3a1bc10b310d450da381e508babd0df7"
        )
        if response.status_code != 200:
            st.error(f"News API request failed with status code: {response.status_code}")
            return

        response = response.json()
        articles = response.get("articles", [])

        if not articles:
            st.info("No news articles available right now.")
            return
    
        return articles

    except Exception as e:
        st.error(f"An error occurred while fetching news data: {e}", icon="🚨")
        return

# get infos of the user like:
# ammount invested in wich active
def user_investiment(actives):
    data = {
        "Actives": [],
        "Position": [],
            }
    
    for key, value in actives.items():
        data["Actives"].append(key)
        data["Position"].append(float(value))

    return data

def distribution(data):
    if not data["Actives"] or not data["Position"]:
            raise(ValueError, "No data to be calculated")
    
    amount = 0.0
    
    for value in data["Position"]:
        amount += value

    porcentage = {}

    for index, active in enumerate(data["Actives"]):
        relative_position = (data["Position"][index] / amount) * 100
        porcentage[active] = f"{relative_position:.2f}%"

    table = pd.Series(porcentage)
    st.write(table)

def main():
    selected = option_menu(
        menu_title = None,
        options = ["Home", "Dashboard"],
        default_index = 0,
        icons = ["house", "currency-dollar"],
        orientation = "horizontal",
    )

    if selected == "Home":
        #getting crypto data for rhen print with make_chart()
        crypto_data = Finance_data(cryptocoins)
        crypto_data.fetch_data()
        crypto_data = crypto_data.process_data()
        make_chart(crypto_data, title="Evolution of Cryptocurrency Prices")

        #getting company data for rhen print with make_chart()
        company_data = Finance_data(companies)
        company_data.fetch_data()
        company_data = company_data.process_data()
        make_chart(company_data, title="Evolution of Company Prices")


        ## News ##

        st.markdown("## Latest News", text_alignment="center")
        
        # what_new() returns the article from top trandings of newsapi, it contains things like:
        # title, image, url of the news, description
        articles = what_new()

        # make 2 columns for print the news side by side
        col1, col2 = st.columns(spec=2, gap="large")


        # it will enumarate wich article with an index, then if this index it`s even the article
        # goes to the left, if it odd goes to the right
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
    

    # if selected the dashboard in the horizontal menu at the top render the dashboard.py file
    if selected == "Dashboard":
        render = st.Page("dashboard.py", title="Finance Dashboard")
        pg = st.navigation([render])
        pg.run()
        investiments = st.multiselect(
            label="Select wich investiments type you currently have",
            options = [
                        "shares",
                        "bonds",
                        "real estate",
                        "mutual funds",
                        "exchange traded funds",
                        "index funds",
                        "real estate investment trusts",
                        "high yield savings accounts",
                        "certificates of deposit",
                        "commodities",
                        "cryptocurrencies",
                        "peer to peer lending",
                        "options",
                        "futures contracts",
                        "precious metals",
                        "collectibles",
                        "currencies",
                        "annuities",
                        "money market funds",
                        "venture capital"
                    ]
            )
        
        actives = {}
        for active in investiments:
            position = st.text_input(
                label=f"Your position in **{active}**", 
                placeholder="10000", 
                icon="💵",
                )

            actives[f"{active}"] = position

        if actives:
            if st.button(
                    label="After fill you positions, click here!", 
                    help="this button will start making your dashboard",
                    icon="🔥",
                    ):
                data = user_investiment(actives)


        # Generating the chart of dashboard
        try:
            if data:
                df = pd.DataFrame(data=data)
                
                df["Position"] = pd.to_numeric(df["Position"])

                st.write(df)
                st.bar_chart(
                    data=df.reset_index(),
                    x="Actives",
                    y="Position",
                    x_label="Actives",
                    y_label="Positions",
                    sort=True,
                    horizontal=True,
                )

                distribution(data)
        
        except Exception as e:
            st.error(f"No data to process yet, press the buttom first: {e}", icon="🚨")
            
            


if __name__ == "__main__":
    main()