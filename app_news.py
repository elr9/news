import streamlit as st
import requests
import openai

BASE_URL = "https://newsapi.org/v2/top-headlines"

def summarize_article(content, description, openai_key):
    openai.api_key = openai_key
    text_to_summarize = content if content and len(content.split()) >= 10 else description
    
    if not text_to_summarize or len(text_to_summarize.split()) < 10 or text_to_summarize.lower() == "[removed]":
        return "Insufficient content for summarization or content not available."

    try:
        response = openai.ChatCompletion.create(
          model="gpt-3.5-turbo",
          messages=[
              {"role": "system", "content": "You are a helpful assistant."},
              {"role": "user", "content": f"Summarize the following article: {text_to_summarize}"}
          ]
        )
        return response['choices'][0]['message']['content'].strip()
    except openai.error.OpenAIError as e:
        return f"Error summarizing article: {str(e)}"

def fetch_headlines(newsapi_key, category=None, country=None, language="en"):
    params = {
        "apiKey": newsapi_key,
        "pageSize": 5,
        "category": category,
        "country": country,
        "language": language
    }
    response = requests.get(BASE_URL, params=params)
    return response.json()

def main():
    st.title("Top 5 Headlines")

    # Sidebar for API key input
    st.sidebar.header("API Key Configuration")
    newsapi_key = st.sidebar.text_input("Enter your NewsAPI Key:", type="password")
    openai_key = st.sidebar.text_input("Enter your OpenAI Key:", type="password")

    # Fetch Newest button
    if st.sidebar.button("Fetch Newest"):
        st.experimental_rerun()

    if not newsapi_key or not openai_key:
        st.warning("Please enter both API keys in the sidebar to fetch and summarize news.")
        return

    # International News
    st.subheader("International News")
    response = fetch_headlines(newsapi_key, language="en")
    articles = response.get("articles", [])
    for idx, article in enumerate(articles):
        button_key = f"international-{idx}-{article['url']}"
        if st.button(article['title'], key=button_key):
            summary = summarize_article(article['content'], article['description'], openai_key)
            st.write(summary)
            st.write(f"[Read the full article]({article['url']})")

    # Mexico News
    st.subheader("Mexico News")
    response = fetch_headlines(newsapi_key, country="fr")
    articles = response.get("articles", [])
    for idx, article in enumerate(articles):
        button_key = f"technology-{idx}-{article['url']}"
        if st.button(article['title'], key=button_key):
            summary = summarize_article(article['content'], article['description'], openai_key)
            st.write(summary)
            st.write(f"[Read the full article]({article['url']})")

    # Technology News
    st.subheader("Technology News")
    response = fetch_headlines(newsapi_key, category="technology", language="en")
    articles = response.get("articles", [])
    for idx, article in enumerate(articles):
        button_key = f"technology-{idx}-{article['url']}"
        if st.button(article['title'], key=button_key):
            summary = summarize_article(article['content'], article['description'], openai_key)
            st.write(summary)
            st.write(f"[Read the full article]({article['url']})")


if __name__ == "__main__":
    main()
