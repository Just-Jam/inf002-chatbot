'''Takes tuple returned by SQL  fetched messages, converts it to dict for AzureOpenAI API usage.'''
def tuple_to_azure_message(message: tuple) -> dict:
    role = message[0]
    if role == 'bot':
        role = 'assistant'
    content = message[1]
    return {
            'role': role,
            'content': [{"type": "text", "text": content}]
    }