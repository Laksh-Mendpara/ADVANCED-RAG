import os
import requests
import json

def gemini_generate_response(prompt):
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        raise ValueError("API Key not found in environment variables.")

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={api_key}"

    headers = {
        "Content-Type": "application/json"
    }

    # Prepare JSON payload
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
        # Send POST request to the Gemini API
        response = requests.post(url, headers=headers, json=payload)

        # Check for HTTP errors
        response.raise_for_status()

        # Parse JSON response
        json_resp = response.json()

        # Validate response and return the content
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


if __name__ == "__main__":
    prompt = "What are the latest developments in AI and technology?"
    response = gemini_generate_response(prompt)
    print("Response from Gemini:", response)
