import streamlit as st
import requests

# Constants
API_KEY = "b3aab8a8dd2c44f38342e65334ec4b0a"
BASE_URL = "https://newsapi.org/v2/top-headlines"
SOURCES = ["bbc-news", "cnn", "the-new-york-times"]  # You can change these to your preferred news outlets

def fetch_headlines(source):
    params = {
        "apiKey": API_KEY,
        "sources": source,
        "pageSize": 5
    }
    response = requests.get(BASE_URL, params=params)
    return response.json().get("articles", [])

def main():
    st.title("Top 5 Headlines from Major News Outlets")

    for source in SOURCES:
        st.subheader(source.replace("-", " ").title())
        articles = fetch_headlines(source)
        for article in articles:
            st.write(f"[{article['title']}]({article['url']})")

if __name__ == "__main__":
    main()
