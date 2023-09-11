import streamlit as st
import requests
import openai

# Constants
NEWSAPI_KEY = "b3aab8a8dd2c44f38342e65334ec4b0a"
OPENAI_KEY = "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"
BASE_URL = "https://newsapi.org/v2/top-headlines"

# Initialize OpenAI
openai.api_key = OPENAI_KEY

def summarize_article(content):
    # Call OpenAI API for summarization using gpt-3.5-turbo
    response = openai.Completion.create(
      engine="gpt-3.5-turbo",
      prompt=f"Summarize the following article: {content}",
      max_tokens=100
    )
    return response.choices[0].text.strip()

def fetch_headlines(category=None, country=None):
    params = {
        "apiKey": NEWSAPI_KEY,
        "pageSize": 5,
        "category": category,
        "country": country
    }
    response = requests.get(BASE_URL, params=params)
    return response.json().get("articles", [])

def main():
    st.title("Top 5 Headlines")

    # International News
    st.subheader("International News")
    articles = fetch_headlines()
    for article in articles:
        st.write(f"[{article['title']}]({article['url']})")
        st.write(summarize_article(article['description']))

    # Mexico News
    st.subheader("Mexico News")
    articles = fetch_headlines(country="mx")
    for article in articles:
        st.write(f"[{article['title']}]({article['url']})")
        st.write(summarize_article(article['description']))

    # Technology News
    st.subheader("Technology News")
    articles = fetch_headlines(category="technology")
    for article in articles:
        st.write(f"[{article['title']}]({article['url']})")
        st.write(summarize_article(article['description']))

if __name__ == "__main__":
    main()
