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
    return 200

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
    page_title="Test",
    page_icon="👋",
)
st.title("Simple chat")
# # Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

chatTopic = sidebar()
azureOpenAI = getAzureopenAI()

if chatTopic:
    # Load chat history for the selected session
    st.session_state.messages = fetchMessagesFromDB(chatTopic)
    azureOpenAI.update_chat_history(st.session_state.messages)
    st.title(f"Chat Session: {chatTopic}")

if chatTopic ==  "":
    st.title(f"Welcome to Info Prof!")
    st.text(f"To get started, create a new chat session on your left!")
    st.text(f"Alternatively, pick up where you left off by selscting a previous chat session!")

# Display chat messages from history on app rerun
for message in st.session_state.messages:
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
    # print('local history ', len(st.session_state.messages))
    # print('db: ', len(load_chat_history(chatTopic)))
    # print(st.session_state.messages)




