# import sqlite3

# con = sqlite3.connect("finance.db")
# cur = con.cursor()

# cur.execute("ALTER TABLE assets ADD COLUMN asset_date DATE DEFAULT CURRENT_DATE;")
# con.commit()
# con.close()
import json
import yfinance as yf

class User_companies:
    def __init__(self, options_shares):
        self._options = []
        self._shares = []
        for option, shares in options_shares.items():
            self._options.append(option)
            self._shares.append(shares)


        self.options = self._options
        self.data = None
        self.amount = self._shares
        self.user_assets = {}
    
    def fetch_company_tickers(self):
        try:
            with open("company_tickers.json", "r") as f:
                companies_tickers = []
                f = json.load(f)

                for value in f.values():
                    if value["ticker"] in self.options:
                        companies_tickers.append(value["ticker"])
                
                return companies_tickers
        except Exception as e:
            return e
        
    def fetch_company_data(self, companies_tickers):
        try:
            self.data = yf.download(companies_tickers, period = "1d")
            self.data = self.data["Close"].iloc[-1]
            return self.data.to_dict()
        except Exception as e:
            return e
    
    def data_to_store(self):

        #for witch ticker that the user own store in a dictionary that info
        index = 0
        for ticker, price in self.data.items():
            self.user_assets[ticker] = {"price": price, "amount": self.amount[index]}
            index = index + 1

        return self.user_assets
    


options_shares = {"TSLA": 119, "AAPL": 987, "MSFT": 897, "GOOGL": 123, "AMZN": 12, "META": 20}
my_companies = User_companies(options_shares)
tk = my_companies.fetch_company_tickers()
my_companies.fetch_company_data(tk)
data = my_companies.data_to_store()
print(data)

# for ticker in data.keys():
            
#     asset_data = data[ticker]
#     price = asset_data.get("price", 0)
#     amount = asset_data.get("amount", 0)
#     print(asset_data, price, amount)


# import yfinance as yf

# # 1. Defina a lista de tickers que você quer
# tickers = ["BTC-USD", "AAPL", "MSFT", "PETR4.SA"]

# # 2. Baixe apenas os dados mais recentes (1 dia de histórico é suficiente)
# dados = yf.download(tickers, period="1d")

# # 3. Pegue apenas a métrica de fechamento ('Close')
# # Como usamos period="1d", pegamos a última linha disponível (.iloc[-1])
# precos_finais = dados['Close'].iloc[-1]

# # 4. Converta a série do Pandas diretamente para um dicionário
# dicionario_precos = precos_finais.to_dict()

# # Mostrando o resultado
# print(dicionario_precos)