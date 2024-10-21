import os
import requests

TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")  

def expand_query(query):
    url = "https://api.together.xyz/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {TOGETHER_API_KEY}",
        "Content-Type": "application/json",
    }

    prompt = f"Given the query: '{query}', extract and list only two separate tasks from this. Each task should be short, distinct, and separated by a comma."

    data = {
        "model": "mistralai/Mixtral-8x7B-Instruct-v0.1",
        "messages": [
            {"role": "system", "content": "Extract two separate tasks."},
            {"role": "user", "content": prompt},
        ]
    }

    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()  
    
    tasks = response.json()["choices"][0]["message"]["content"].split(',')
    tasks = [task.strip() for task in tasks if task.strip()]
    return tasks

def decompose_query(query):
    tasks = expand_query(query)
    return tasks

if __name__ == "__main__":
    test_query = input("Enter a query to expand and decompose: ")


    tasks = decompose_query(test_query)

    print("Decomposed Sub-Queries (Tasks):")
    print(tasks)
