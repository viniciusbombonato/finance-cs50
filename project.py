import altair as alt
import bcrypt as bc
import json
import pandas as pd
import requests
import streamlit as st
from streamlit_option_menu import option_menu
import sqlite3
import yfinance as yf


cryptocoins = ["BTC-USD"]
companies = ["TSLA", "AAPL", "MSFT", "GOOGL", "AMZN", "META"]

class Finance_data:
    def __init__(self, tickers, period="1mo"):
        self.tickers = tickers
        self.period = period
        self.data = None

    def fetch_data(self):
        try:
            self.data = yf.download(self.tickers, group_by="ticker", period=self.period)
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

class User_companies:
    def __init__(self, options_shares):
        self._options = list(options_shares.keys())
        self._shares = list(options_shares.values())

        self.data = None
        self.user_assets = {}

    def fetch_company_tickers(self):
        try:
            companies_tickers = []
            with open("name_ticker.json", "r") as f:
                companies_tickers = []
                f = json.load(f)

                for name, ticker in f.items():
                    if name in self._options:
                        companies_tickers.append(ticker)
                
            return companies_tickers
            
        except FileNotFoundError as e:
            raise FileNotFoundError("The filfe \" name_ticker.json\" was not found") from e
        except json.JSONDecodeError as e:
            raise ValueError("Error while trying to decode json file, check the format") from e
        except (AttributeError, KeyError) as e:
            raise ValueError("Not a Dictionarie, check the format") from e
        except Exception as e:
            raise ValueError("An error occur") from e
             
        
    def fetch_company_data(self, companies_tickers):
        try:
            self.data = yf.download(companies_tickers, period = "1d")
            self.data = self.data["Close"].iloc[-1]
            self.data = self.data.to_dict()

            return self.data
        
        except RuntimeError as e:
            raise RuntimeError("Error on yfinance API")  from e
        except (ValueError, AttributeError) as e:
            raise ValueError(f"Could not fomart the data, check if it is indeed a dictionarie: {e}") from e
        except Exception as e:
            raise ValueError("An error occur") from e
    
    def data_to_store(self):

        #for witch ticker that the user own store in a dictionary that info
        index = 0
        for ticker, price in self.data.items():
            self.user_assets[ticker] = {"price": price, "amount": self._shares[index]}
            index = index + 1

        return self.user_assets



def register(username, password1, password2):

    if username and password1 and password2:
        
        # check if passwords are the same
        if password1 == password2:

            # try to connect with sata base and check if user already exist
            try:
                con = sqlite3.connect("finance.db")
                cur = con.cursor()
                cur.execute("SELECT * FROM users WHERE user_name = ?", (username,))
                res = cur.fetchone()

            except Exception as e:
                return e
            
            # if no user with this username was found, insert new user into table
            if not res:
                password1 = password1.encode("utf-8")
                hashed = bc.hashpw(password1, bc.gensalt())
                
                cur.execute("INSERT INTO users (user_name, user_password) VALUES (?, ?);", (username, hashed,))                           
                con.commit()
                con.close()
                
                #check if new user was register
                try:
                    new_con = sqlite3.connect("finance.db")
                    new_cur = new_con.cursor()
                    new_cur.execute("SELECT * FROM users WHERE user_name = ?", (username,))
                    new_res = new_cur.fetchone()

                    if not new_res:
                        register(username, password1, password2)

                    else:
                        new_con.close()
                        return 0
                    
                except Exception as e: 
                    return e

                return 0
            else:
                return f"User already exists"
        else:
            return f"Password not Matches"
    else:
        return f"Insert your username and password"

def login(username, password):
    
    # connect with data base
    try:
        con = sqlite3.connect("finance.db")
        cur = con.cursor()
    except Exception as e:
        return e

    #hash password
    password = password.encode("utf-8")

    cur.execute("""
                SELECT * 
                FROM users
                WHERE user_name = ?
                        """, (username,))
    res = cur.fetchone()
    
    if res:
        if username == res[1]:
            if bc.checkpw(password, res[2]):
                return 0
            else:
                return 2
    else:
        return 1

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

def yf_companies_names():
    with open("name_ticker.json", "r") as f:
        f = json.load(f)
        companies_names = []

        for key in f.keys():
            companies_names.append(key)
        
        return companies_names

def get_user_id(user_for_dash):
    with sqlite3.connect("finance.db") as con:
        cur = con.cursor()

        cur.execute("SELECT user_id FROM users WHERE user_name = ?", (user_for_dash,))
        res = cur.fetchone()

        if res is None:
            return f"User \`{user_for_dash}\` not found."
        
        user_id = res[0]
        return user_id

def users_assets_check(con, user_id, ticker, current_price, current_amount):
    cur = con.cursor()

    cur.execute(
        """
        SELECT asset_price, asset_amount 
        FROM assets 
        WHERE asset_ticker = ? AND user_id = ?
        """, (ticker, user_id))
    res = cur.fetchone()

    if res is None:
        return 0 

    old_price, old_amount = res[0], res[1]
    amount_purchase = current_amount - old_amount
    total_price = (old_amount * old_price) + (current_price * amount_purchase)
    average_price = total_price / current_amount if current_amount > 0 else 0

    cur.execute(
        """
        UPDATE assets 
        SET asset_price = ?, asset_amount = ?, average_price = ?, asset_date = CURRENT_DATE
        WHERE user_id = ? AND asset_ticker = ?
        """,
        (current_price, current_amount, average_price, user_id, ticker)
    )
    return 1  

def store_companies(user_assets, user_id):
    try:
        
        with sqlite3.connect("finance.db") as con:
            cur = con.cursor()

            for ticker, asset_data in user_assets.items():
                price = asset_data.get("price", 0)
                amount = asset_data.get("amount", 0)

                check_asset = users_assets_check(con, user_id, ticker, price, amount)

                if check_asset == 0:
                    cur.execute("""
                        INSERT INTO assets (user_id, asset_ticker, asset_price, asset_amount, average_price)
                        VALUES (?, ?, ?, ?, ?)
                    """, (user_id, ticker, price, amount, price))
            
            con.commit()
            st.success("All Done!")
            return True

    except Exception as e:
        return f"An error occured: {e}"

def get_user_assets(user_id):
    with sqlite3.connect("finance.db") as con:
        cur = con.cursor()

        cur.execute("SELECT asset_ticker, average_price FROM assets WHERE user_id = ?", (user_id,))
        res = cur.fetchall()
        if res:
            return res
        else:
            return 1 #user don't have any asset

def make_user_dict(assets_info, tickers_price):
    user_dict_toDash = {}
    for ticker, avrPrice in assets_info:
        for nowTicker, nowPrice in tickers_price.items():
            if ticker == nowTicker:
                user_dict_toDash[ticker] = [avrPrice, nowPrice]

    return user_dict_toDash


def dict_to_df(dict):
    
    dict = pd.DataFrame(dict, index=(["Average", "Current"]))
    return dict

def get_tickers_for_dash(list_ticker_avPrice):
    user_tickers = []

    for asset in list_ticker_avPrice:
        user_tickers.append(asset[0])
    
    return user_tickers

def get_price_from_data(data):
    data =  data["Close"].iloc[-1]
    data = data.to_dict()

    return data



def main():
    if 'logged' not in st.session_state:
        st.session_state['logged'] = False
    if "register" not in st.session_state:
        st.session_state["register"] = False
    if "register_layout" not in st.session_state:
        st.session_state["register_layout"] = False
    if "login_layout" not in st.session_state:
        st.session_state["login_layout"] = True

    if "username" not in st.session_state:
        st.session_state["username"] = None


    if st.session_state['logged'] == True:

        #get user name and ID
        user_for_dash = st.session_state["username"]
        user_id = get_user_id(user_for_dash)
    
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
    

        # if selected the dashboard in the horizontal menu at the top, render the dashboard.py file
        if selected == "Dashboard":
            render = st.Page("dashboard.py", title="Finance Dashboard")
            pg = st.navigation([render])
            pg.run()

            companies_names = yf_companies_names()

            options = st.multiselect(
                label="Select your assets",
                options=companies_names,
                key="user_companies_options",
            )


            if options:
                shares_holding = {}
                all_filled = True
                for option in options:
                    shares_amount = st.number_input(
                        label=f"how many shares do you have of **{option}** ?",
                        value=None,
                        key=f"{option}_key",
                    )
                    
                    if shares_amount:
                        shares_holding[option] = shares_amount
                    else:
                        all_filled = False

                done = st.button(label="Done")


                if done:
                    if all_filled and shares_holding:

                        assets_info = User_companies(shares_holding)

                        try:
                            tk = assets_info.fetch_company_tickers()
                            assets_info.fetch_company_data(tk)
                            user_assets_dict = assets_info.data_to_store()
                        except Exception as err:
                            st.error(err)
 
                        # after filtering the users assets now it stores into DB
                        results = store_companies(user_assets_dict, user_id)
                        if results != True:
                            st.error(results)
                    else:
                        st.error("Please fill the share amounts for all selected options.")

            user_assets_info = get_user_assets(user_id)
            if user_assets_info:
                user_tickers = get_tickers_for_dash(user_assets_info)

                user_tickers_price = User_companies(options_shares={})
                user_tickers_price = user_tickers_price.fetch_company_data(user_tickers)

                if isinstance(user_tickers_price, dict):
                    dict_to_print = make_user_dict(user_assets_info, user_tickers_price)
                    st.write(dict_to_df(dict_to_print))
                    
                else:
                    st.error(f"Could not fetch ticker prices: {user_tickers_price}")


                # About the average price and current price for the user's assets
                with st.container(border=True):
                    st.subheader("📊 Understanding Your Portfolio Metrics")
                    st.markdown(
                        """
                        Your **Average Price** (cost basis) represents the mean amount you paid per share across all purchases. 
                        Comparing this to the **Current Market Price** gives you an instant snapshot of your investment's real-time performance.
                        """
                    )

                st.divider()

                st.markdown("### 💡 Price Comparison Quick Guide")

                col1, col2, col3 = st.columns(3)

                with col1:
                    st.success("##### 🟢 Below Current Price")
                    st.metric(
                        label="Status",
                        value="In Profit",
                        delta="Avg < Current",
                        delta_color="normal",
                    )
                    st.caption(
                        "The market values the stock **higher** than what you paid for it. Your position is currently in the green!"
                    )

                with col2:
                    st.info("##### 🔵 Equal to Current Price")
                    st.metric(
                        label="Status",
                        value="Breakeven",
                        delta="Avg == Current",
                        delta_color="off",
                    )
                    st.caption(
                        "You have neither gained nor lost value relative to your initial entry point."
                    )

                with col3:
                    st.error("##### 🔴 Above Current Price")
                    st.metric(
                        label="Status",
                        value="Unrealized Loss",
                        delta="- Avg > Current",
                        delta_color="inverse",
                    )
                    st.caption(
                        "The market is trading **below** your average purchase price. Your position is currently in the red."
                    )

                
                st.toast("💡 Remember: Gains or losses remain unrealized until you sell!")



            elif user_assets_info == 1:
                st.error("user [{user_for_dash}] not found")
                    



     # if user not logged, send him to login page   
    elif st.session_state['logged'] == False and st.session_state["login_layout"] == True:
        render = st.Page("login.py", title="Login")
        pg = st.navigation([render])
        pg.run()

        #forms to log user
        with st.form("login_forms"):
            st.markdown("## Log In")
            username = st.text_input(
                label = "Username",
                max_chars = 30,
                )
            password = st.text_input(
                label = "Password",
                type = "password",
                )
            log_user = st.form_submit_button(
                label="Log In"
            )
            #set the session as log if all went right
            if log_user:
                check_login = login(username, password)
                if check_login == 0:
                    st.session_state["logged"] = True
                    st.session_state["login_layout"] = False 
                    st.session_state["username"] = username
                elif check_login == 1:
                    st.error(f"No user found it", icon="🚨")
                elif check_login == 2:
                    st.error(f"wrong password", icon="🚨")

        # in case the user doesn't have a login
        st.write("Do not have a login yet?")
        not_logged = st.button (
            label="Register"
        )
        if not_logged:
            st.session_state["register_layout"] = True
            st.session_state["register"] = True
            st.session_state["login_layout"] = False
            

    elif st.session_state["register"] == True and st.session_state["register_layout"] == True:
        render = st.Page("register.py", title="Register")
        pg = st.navigation([render])
        pg.run()

        #forms to register the user
        with st.form("register_forms"):
            st.markdown("## Register")
            username = st.text_input(
                label = "Username",
                max_chars = 30,
                )
            password1 = st.text_input(
                label = "Password",
                type = "password",
                )
            password2 = st.text_input(
                label = "Repeat your password",
                type = "password",
                )
            register_button = st.form_submit_button(
                label="Register"
            )

            #see if user was register correctly
            if register_button:
                register_user = register(username, password1, password2)
                if register_user == 0:
                    st.session_state["logged"] = True
                    st.session_state["register"] = False
                    st.session_state["register_layout"] = False
                    st.session_state["login_layout"] = False 
                    st.session_state["username"] = username
                
                else:
                    st.write(f"{register_user}")
            
        st.write("Already have an account?")
        have_account = st.button("Log in")

        if have_account:
            st.session_state["register"] = False
            st.session_state["register_layout"] = False
            st.session_state["login"] = True
            st.session_state["login_layout"] = True


if __name__ == "__main__":
    main()