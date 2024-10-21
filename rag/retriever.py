import os
import json
import requests
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from transformers import DistilBertModel, DistilBertTokenizer
import torch
from data import fetch_news, store_articles 

tokenizer = DistilBertTokenizer.from_pretrained('distilbert-base-uncased')
model = DistilBertModel.from_pretrained('distilbert-base-uncased')

def embed_text(text):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=512)
    with torch.no_grad():
        outputs = model(**inputs)
        embedding = torch.mean(outputs.last_hidden_state, dim=1).squeeze().tolist()
    return embedding

def fetch_and_store_news(query):
   
    articles = fetch_news(query)
    store_articles(articles)
    return articles

def retrieve_news(query):
    query_embedding = embed_text(query)
    articles = load_articles()

    if not articles:
        print("No articles found in the database.")
        return []

    article_embeddings = []
    for article in articles:
        article_embedding = embed_text(article['title'])
        article_embeddings.append(article_embedding)

    similarities = cosine_similarity([query_embedding], article_embeddings)[0]

    top_indices = similarities.argsort()[-5:][::-1]
    relevant_articles = [articles[i] for i in top_indices]

    return relevant_articles

def load_articles():
    
    if os.path.exists("data/retrieved_news.json"):
        with open("data/retrieved_news.json", "r") as f:
            return json.load(f)
    return []

if __name__ == "__main__":
    test_query = "Latest developments in AI and technology"
    print(f"Testing retrieval with query: '{test_query}'")

    articles = fetch_and_store_news(test_query)
    print(f"Fetched {len(articles)} articles.")

    relevant_articles = retrieve_news(test_query)
    print(f"Retrieved {len(relevant_articles)} relevant articles.")
    print(relevant_articles)
