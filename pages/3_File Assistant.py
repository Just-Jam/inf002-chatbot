from cProfile import label

import streamlit as st
import time
import uuid
from api.azure import AzureOpenAI
from components.sidebar import sidebar
from database import load_chat_history, save_msg, clear_chat_history
from utils.sql_api_utils import tuple_to_azure_message
# import streamlit_js_eval

def file_upload():
    if 'uploaded_file' not in st.session_state:
        st.session_state.uploaded_file_content = None  # Stores the content of the uploaded file

    if 'file_uploaded_message_shown' not in st.session_state:
        st.session_state.file_uploaded_message_shown = False  # Flag to show upload message only once

        # File Upload
    uploaded_file = st.file_uploader("Upload a text file", type=["txt", "pdf"])  # Allow user to upload a text fil

    if uploaded_file:
        st.session_state.uploaded_file_content = uploaded_file.read().decode('utf-8')  # Read and decode the uploaded file
        print("2. Uploaded file: ", st.session_state.uploaded_file_content)
        # Show upload message only once
        if not st.session_state.file_uploaded_message_shown:
            st.markdown("File uploaded successfully. What do you want to do with the file?",unsafe_allow_html=True)
            st.session_state.file_uploaded_message_shown = True

        if st.button("Summarize"):
            summarize_text(st.session_state.uploaded_file_content)



# @st.cache_resource
def  getAzureopenAI():
    azureOpenAI = AzureOpenAI()
    return azureOpenAI

def syncMessagesWithDB(messages: list):
    for message in messages:
        role = message['role']
        content = message['content'][0]['text']
        save_msg(chatTopic, role, content, GROUP_ID)
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

def summarize_text(content):
    prompt = f"Summarize the following text: {content}"
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        response = st.write_stream(response_generator(prompt, azureOpenAI=azureOpenAI))
    # Add assistant response to chat history
    assistant_message = {
        'role': 'assistant',
        'content': [{"type": "text", "text": response}]
    }

    syncMessagesWithDB([assistant_message])


st.set_page_config(
    page_title="File Assistant",
    page_icon="👋",
)

GROUP_ID = "file_assistant"
chatTopic = sidebar(GROUP_ID)
azureOpenAI = getAzureopenAI()
messages = []
file_upload()

if chatTopic:
    # Load chat history for the selected session
    messages = fetchMessagesFromDB(chatTopic)
    azureOpenAI.update_chat_history(messages)
    st.title(f"Chat Session: {chatTopic}")
    #Remove system message
    messages.pop(0)


if chatTopic ==  "":
    st.title(f"Welcome to File Assistant!")
    st.text(f"To get started, create a new chat session on your left!")
    st.text(f"Alternatively, pick up where you left off by selecting a previous chat session!")

# Display chat messages from history
for message in messages:
    message_content = message["content"][0]['text']
    with st.chat_message(message["role"]):
        col1, col2 = st.columns([9,1])
        with col1:
            st.markdown(message_content)
        with col2:
            if st.button(label="TTS", key=uuid.uuid4(), use_container_width=True):
                print("TTS")

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