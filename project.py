import requests
import streamlit as st

def main():
    payload={
        'start': '1',
        'limit': '10',
        'convert': 'USD',
        'fields': 'symbol, price, market_cap'
    }
    headers = {
        'Accept': 'application/json',
        'X-CMC_PRO_API_KEY': 'f5148270e8f24a0e95bd33d8cecee932',
    }
    url = 'https://pro-api.coinmarketcap.com/v3/cryptocurrency/listings/latest'

    response = requests.get(url, params=payload, headers=headers)
    content = response.json()

    for item in content['data']:
        quote = item.get('quote', [])
        price = quote[0].get('price') if quote else None
        price = round(price, 2)
        print(f"{item['name']}: {price}")

if __name__ == "__main__":
    main()