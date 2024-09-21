import os
import requests
import base64
from dotenv import load_dotenv
import json

load_dotenv()
class AzureOpenAI:
    API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
    ENDPOINT = "https://openaisit.openai.azure.com/openai/deployments/gpt-4o-mini-25k/chat/completions?api-version=2024-02-15-preview"
    DEFAULT_SYS_MESSAGE: str = "You are an AI assistant that helps people find information."

    def __init__(self):
        self._messages:list[dict] = [
            {"role": "system", "content": [{"type": "text", "text": self.DEFAULT_SYS_MESSAGE}]}
        ]
    def generate_response_gpt4om(self, prompt: str):
        headers = {
            "Content-Type": "application/json",
            "api-key": self.API_KEY,
        }

        self._messages.append(
            {'role': 'user', 'content': [{"type": "text", "text": prompt}]}
        )
        payload = {
            "messages": self._messages,
            "temperature": 0.7,
            "top_p": 0.95,
            "max_tokens": 800
        }
        # Send request
        try:
            response = requests.post(self.ENDPOINT, headers=headers, json=payload)
            response.raise_for_status()  # Will raise an HTTPError if the HTTP request returned an unsuccessful status code
        except requests.RequestException as e:
            raise SystemExit(f"Failed to make the request. Error: {e}")

        self._messages.append(
            {"role": "assistant", "content": [
                    {"type": "text", "text": response.json()['choices'][0]['message']['content']}
                ]
            }
        )

        return response.json()['choices'][0]['message']['content']

    def get_chat_history(self) -> list[dict]:
        return self._messages

