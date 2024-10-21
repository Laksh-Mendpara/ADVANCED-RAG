import os
import json
import requests
from typing import List


def gemini_generate_response(prompt: str) -> str:
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        raise ValueError("API Key not found in environment variables.")

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={api_key}"
    headers = {
        "Content-Type": "application/json"
    }

    payload = {
        "contents": [
            {
                "parts": [
                    {
                        "text": prompt
                    }
                ]
            }
        ]
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()

        json_resp = response.json()
        if (
            "candidates" in json_resp and
            isinstance(json_resp["candidates"], list) and
            json_resp["candidates"]
        ):
            return json_resp["candidates"][0]["content"]["parts"][0]["text"]
        else:
            return "Error: Invalid response format."
    
    except requests.exceptions.HTTPError as http_err:
        return f"HTTP error occurred: {http_err}"
    except json.JSONDecodeError:
        return "Error decoding JSON response."
    except Exception as err:
        return f"An error occurred: {err}"


def process_prompts(prompts: List[str]) -> None:
    """
    Process multiple prompts by generating responses for each.
    
    Args:
    prompts (List[str]): A list of text prompts to process.
    """
    for prompt in prompts:
        response = gemini_generate_response(prompt)
        print(f"Prompt: {prompt}\nResponse: {response}\n")


if __name__ == "__main__":
    prompts = input("Enter prompts separated by commas: ").split(',')
    prompts = [prompt.strip() for prompt in prompts] 
    process_prompts(prompts)
