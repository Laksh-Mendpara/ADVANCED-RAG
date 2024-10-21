import os
import json
import requests

news_api_key = os.getenv("NEWS_API_KEY")
NEWS_API_URL = "https://newsapi.org/v2/everything"

def fetch_news(query):
    params = {
        "q": query,
        "apiKey": news_api_key,
        "language": "en",
        "pageSize": 5
    }
    response = requests.get(NEWS_API_URL, params=params)
    articles = response.json().get("articles", [])
    return articles

def store_articles(articles):
    os.makedirs("data", exist_ok=True) 
    
    existing_articles = []
    if os.path.exists("data/retrieved_news.json"):
        with open("data/retrieved_news.json", "r") as f:
            existing_articles = json.load(f)

    existing_articles.extend(articles)

    with open("data/retrieved_news.json", "w") as f:
        json.dump(existing_articles, f, indent=4) 


def load_articles():
    
    if os.path.exists("data/retrieved_news.json"):
        with open("data/retrieved_news.json", "r") as f:
            return json.load(f)
    return []
