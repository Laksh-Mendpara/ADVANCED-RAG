from query import decompose_query
from retriever import fetch_and_store_news, retrieve_news
from agent import gemini_generate_response

def news_pipeline(query):
    
    sub_queries = decompose_query(query)
    print(f"Decomposed Sub-Queries: {sub_queries}")
    
    all_articles = []
    for sub_query in sub_queries:
        articles = fetch_and_store_news(sub_query)
        all_articles.append(articles)
        print(f"Fetched {len(articles)} articles for sub-query : {sub_query}")
        
    print("Step 3: Retrieving ranked news articles.")
    relevant_articles = retrieve_news(query)
    print(f"Retrieved {len(relevant_articles)} relevant articles for the query: '{query}'")

    summaries = [article['description'] for article in relevant_articles]
    context = " ".join(summaries)
    final_response = gemini_generate_response(f"Summarize the following articles and write ourput saying the current news in this field and give output in paragraph form: {context}")
    
    return final_response

if __name__ == "__main__":
    query = input("Enter query: ")
    response = news_pipeline(query)

    print()
    print()
    print()
    print()
    print()
    print()
    
    print("Final Summarized Response:")
    print(response)
