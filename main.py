import streamlit as st
import time
import uuid
from api.azure import AzureOpenAI
from sidebar import  sidebar
from database import load_chat_history, save_msg, clear_chat_history
from utils.sql_api_utils import tuple_to_azure_message
import streamlit_js_eval

# @st.cache_resource
def  getAzureopenAI():
    azureOpenAI = AzureOpenAI()
    return azureOpenAI

def syncMessagesWithDB(messages: list):
    for message in messages:
        role = message['role']
        content = message['content'][0]['text']
        msg_uuid = uuid.uuid4()
        save_msg(str(msg_uuid), chatTopic, role, content)
    return True

def fetchMessagesFromDB(chatTopic):
    chat_history = load_chat_history(chatTopic)
    messages = []
    for entry in chat_history:
        messages.append(tuple_to_azure_message(entry))
    return messages

def response_generator(prompt, azureOpenAI):
    response = azureOpenAI.generate_response_gpt4om(prompt)
    for word in response.split():
        yield word + " "
        time.sleep(0.05)

st.set_page_config(
    page_title="Chat",
    page_icon="👋",
)

chatTopic = sidebar()
azureOpenAI = getAzureopenAI()
messages = []

if chatTopic:
    # Load chat history for the selected session
    messages = fetchMessagesFromDB(chatTopic)
    azureOpenAI.update_chat_history(messages)
    st.title(f"Chat Session: {chatTopic}")
    #Remove system message
    messages.pop(0)

if chatTopic ==  "":
    st.title(f"Welcome to Info Prof!")
    st.text(f"To get started, create a new chat session on your left!")
    st.text(f"Alternatively, pick up where you left off by selscting a previous chat session!")

# Display chat messages from history
for message in messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"][0]['text'])

if chatTopic != "" and st.button("Clear Chat History"):
    print(chatTopic)
    clear_chat_history(chatTopic)
    time.sleep(2)
    st.success("History Cleared!")
    # streamlit_js_eval(js_expressions="parent.window.location.reload()")

# Accept user input
if prompt := st.chat_input("What is up?"):
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    # Add user message to chat history
    user_message = {
        'role': 'user',
        'content': [{"type": "text", "text": prompt}]
    }

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        response = st.write_stream(response_generator(prompt, azureOpenAI=azureOpenAI))
    # Add assistant response to chat history
    assistant_message = {
        'role': 'assistant',
        'content': [{"type": "text", "text": response}]
    }

    syncMessagesWithDB([user_message, assistant_message])

    # print("azure ", len(azureOpenAI.get_chat_history()))
    # print('db: ', len(load_chat_history(chatTopic)))
    # print(load_chat_history(chatTopic))