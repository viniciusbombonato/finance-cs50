from newsapi import NewsApiClient
import streamlit as st
import requests



response = requests.get('https://newsapi.org/v2/top-headlines?country=us&apiKey=3a1bc10b310d450da381e508babd0df7')
response = response.json()



for article in response['articles']:
    st.markdown("## " + article['title'])
    if article['urlToImage']:
        st.image(image=article['urlToImage'])
    st.write(article['description'])
