import os
from openai import OpenAI
from dotenv import load_dotenv

# Load values from the .env file if it exists
load_dotenv()

# Configure OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Constants for the chat
TEMPERATURE = 0.5
MAX_TOKENS = 500
FREQUENCY_PENALTY = 0
PRESENCE_PENALTY = 0.6

def get_response(messages):
    """Get a response from ChatCompletion."""
    response = client.chat.completions.create(
        model='gpt-4o-mini',  # Keep your original model here
        messages=messages,
        temperature=TEMPERATURE,
        max_tokens=MAX_TOKENS,
        frequency_penalty=FREQUENCY_PENALTY,
        presence_penalty=PRESENCE_PENALTY,
    )
    return response.choices[0].message.content

def main():
    os.system("cls" if os.name == "nt" else "clear")
    conversation_history = ""  # Store entire conversation history
    last_response = ""  # Track last response separately

    while True:
        user_prompt = input("Prompt:\n")
        
        # Replace 'previous result' with the last response
        if "previous result" in user_prompt.lower() and last_response:
            user_prompt = user_prompt.replace("previous result", last_response.strip())

        # Build the conversation history
        conversation_history += f"User: {user_prompt}\n"

        # Prepare the chat message structure with conversation history and user input
        messages = [
            {'role': 'user', 'content': conversation_history}
        ]

        # Get the response from the API
        response = get_response(messages)

        # Append the assistant's response to the conversation history
        conversation_history += f"{response}\n"
        
        # Update last response for future reference
        last_response = response.strip()

        # Print the response
        print(response)

if __name__ == "__main__":
    main()
