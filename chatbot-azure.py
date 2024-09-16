import os
import requests
import base64
from dotenv import load_dotenv
import json

def main():
    # Configuration
    load_dotenv()
    API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
    # IMAGE_PATH = "YOUR_IMAGE_PATH"
    # encoded_image = base64.b64encode(open(IMAGE_PATH, 'rb').read()).decode('ascii')
    headers = {
        "Content-Type": "application/json",
        "api-key": API_KEY,
    }

    user_prompt = input("Prompt:\n")

    messages: list[dict] = [
        {"role": "system", "content": [{"type": "text", "text": "You are an AI assistant that helps people find information."}]},
        {'role': 'user', 'content': [{"type": "text", "text": user_prompt}]}
    ]

    # Payload for the request
    payload = {
      "messages": messages,
      "temperature": 0.7,
      "top_p": 0.95,
      "max_tokens": 800
    }

    ENDPOINT = "https://openaisit.openai.azure.com/openai/deployments/gpt-4o-mini-25k/chat/completions?api-version=2024-02-15-preview"

    # Send request
    try:
        response = requests.post(ENDPOINT, headers=headers, json=payload)
        response.raise_for_status()  # Will raise an HTTPError if the HTTP request returned an unsuccessful status code
    except requests.RequestException as e:
        raise SystemExit(f"Failed to make the request. Error: {e}")

    # Handle the response as needed (e.g., print or process)
    # print(response.json())
    print(response.json()['choices'][0]['message']['content'])
    with open('response.json', 'w') as f:
        json.dump(response.json(), f)

if __name__ == '__main__':
    main()