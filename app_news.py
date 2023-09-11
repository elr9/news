import streamlit as st
import requests
import openai

BASE_URL = "https://newsapi.org/v2/top-headlines"

def summarize_article(content, openai_key):
    openai.api_key = openai_key
    try:
        response = openai.ChatCompletion.create(
          model="gpt-3.5-turbo",
          messages=[
              {"role": "system", "content": "You are a helpful assistant."},
              {"role": "user", "content": f"Summarize the following article: {content}"}
          ]
        )
        return response['choices'][0]['message']['content'].strip()
    except openai.error.OpenAIError as e:
        return f"Error summarizing article: {str(e)}"


def fetch_headlines(newsapi_key, category=None, country=None):
    params = {
        "apiKey": newsapi_key,
        "pageSize": 5,
        "category": category,
        "country": country
    }
    response = requests.get(BASE_URL, params=params)
    return response.json().get("articles", [])

def main():
    st.title("Top 5 Headlines")

    # Sidebar for API key input
    st.sidebar.header("API Key Configuration")
    newsapi_key = st.sidebar.text_input("Enter your NewsAPI Key:", type="password")
    openai_key = st.sidebar.text_input("Enter your OpenAI Key:", type="password")

    if not newsapi_key or not openai_key:
        st.warning("Please enter both API keys in the sidebar to fetch and summarize news.")
        return

    # International News
    st.subheader("International News")
    articles = fetch_headlines(newsapi_key)
    for article in articles:
        st.write(f"[{article['title']}]({article['url']})")
        st.write(summarize_article(article['description'], openai_key))

    # Mexico News
    st.subheader("Mexico News")
    articles = fetch_headlines(newsapi_key, country="mx")
    for article in articles:
        st.write(f"[{article['title']}]({article['url']})")
        st.write(summarize_article(article['description'], openai_key))

    # Technology News
    st.subheader("Technology News")
    articles = fetch_headlines(newsapi_key, category="technology")
    for article in articles:
        st.write(f"[{article['title']}]({article['url']})")
        st.write(summarize_article(article['description'], openai_key))

if __name__ == "__main__":
    main()
