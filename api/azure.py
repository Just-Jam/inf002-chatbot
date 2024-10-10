import os
import requests
from dotenv import load_dotenv
from openai import AzureOpenAI as AOI
import json
import httpx
import uuid

'''
This class handles AzureOpenAI chatbot api calls. The class itself handles and stores up to 20 previous messages.
generate_response_gpt4om() updates conversation history and returns the latest chatbot response.

Ussage:
import AzureOpenAI
azureOpenAI = AzureOpenAI()
azureOpenAI.generate_response_gpt4om(prompt)
'''

load_dotenv()

class AzureOpenAI:
    API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
    ENDPOINT = "https://openaisit.openai.azure.com/"
    GPT_4OM_ENDPOINT = "https://openaisit.openai.azure.com/openai/deployments/gpt-4o-mini-25k/chat/completions?api-version=2024-02-15-preview"
    EMBEDDING_ENDPOINT = "https://openaisit.openai.azure.com/openai/deployments/text-embedding-3-small/embeddings?api-version=2023-05-15"
    DEFAULT_SYS_MESSAGE: str = "You are an AI assistant that helps people find information.1"
    MAX_MESSAGE_COUNT = 30

    def __init__(self):
        self._messages: list[dict] = [
            {
                "role": "system",
                "content": [{"type": "text", "text": self.DEFAULT_SYS_MESSAGE}]
            }
        ]

    def generate_response_gpt4om(self, prompt: str):
        headers = {
            "Content-Type": "application/json",
            "api-key": self.API_KEY,
        }

        self._messages.append(
            {
                'role': 'user',
                'content': [{"type": "text", "text": prompt}]
            }
        )

        payload = {
            "messages": self._messages,
            "temperature": 0.7,
            "top_p": 0.95,
            "max_tokens": 800
        }
        # Send request
        try:
            response = requests.post(self.GPT_4OM_ENDPOINT, headers=headers, json=payload)
            response.raise_for_status()  # Will raise an HTTPError if the HTTP request returned an unsuccessful status code
        except requests.RequestException as e:
            raise SystemExit(f"Failed to make the request. Error: {e}")

        self._messages.append(
            {
                "role": "assistant",
                "content": [{"type": "text", "text": response.json()['choices'][0]['message']['content']}]
             }
        )

        if len(self._messages) > self.MAX_MESSAGE_COUNT:
            self._messages.pop(1)
            self._messages.pop(1)

        return response.json()['choices'][0]['message']['content']

    def get_chat_history(self) -> list[dict]:
        return self._messages

    def update_chat_history(self, messages: list[dict]):
        self._messages = messages
        return True

    # def generate_embeddings(self, file):
    #     embeddings = AzureOpenAIEmbeddings(
    #         model= "text-embedding-3-small",
    #         azure_endpoint= self.EMBEDDING_ENDPOINT,
    #         api_key= self.API_KEY
    #     )
    #     # print(embeddings)
    #     return "In Progress"
    def generate_image_dalle3(self, prompt: str):
        client = AOI(
            api_version="2024-02-01",
            api_key=self.API_KEY,
            azure_endpoint=self.ENDPOINT
        )

        result = client.images.generate(
            model="dall-e-3",  # the name of your DALL-E 3 deployment
            prompt=prompt,
            n=1
        )

        # Set the directory for the stored image
        image_dir = os.path.join(os.curdir, 'images')

        # If the directory doesn't exist, create it
        if not os.path.isdir(image_dir):
            os.mkdir(image_dir)

        # Initialize the image path (note the filetype should be png)
        image_path = os.path.join(image_dir, f'image_{uuid.uuid4()}.png')

        # Retrieve the generated image
        json_response = json.loads(result.model_dump_json())
        image_url = json_response["data"][0]["url"]  # extract image URL from response
        generated_image = httpx.get(image_url).content  # download the image
        with open(image_path, "wb") as image_file:
            image_file.write(generated_image)

        return image_path