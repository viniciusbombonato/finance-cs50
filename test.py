import pandas as pd

data = {
    "Actives": [
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
    ],
    "Position": [
        15000.50,  # shares
        8000.00,   # bonds
        120000.00, # real estate
        5000.00,   # mutual funds
        25000.75,  # exchange traded funds
        35000.00,  # index funds
        12000.30,  # real estate investment trusts
        4500.00,   # high yield savings accounts
        10000.00,  # certificates of deposit
        3000.00,   # commodities
        2500.25,   # cryptocurrencies
        1500.00,   # peer to peer lending
        400.00,    # options
        0.00,      # futures contracts
        6000.00,   # precious metals
        2000.00,   # collectibles
        1100.00,   # currencies
        9000.00,   # annuities
        7500.00,   # money market funds
        0.00       # venture capital
    ]
}

if not data["Actives"] or not data["Position"]:
        raise(ValueError, "No data to be calculated")

amount = 0.0

for value in data["Position"]:
    amount += value

porcentage = {}

for index, active in enumerate(data["Actives"]):
    relative_position = (data["Position"][index] / amount) * 100
    porcentage[active] = f"{relative_position:.2f}%"

series = pd.Series(porcentage)

print(series)

