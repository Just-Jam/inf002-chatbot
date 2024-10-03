import streamlit as st
import time
import uuid
import os
from api.azure import AzureOpenAI
from components.sidebar import sidebar
from components.file_upload import file_upload
from database import load_chat_history, save_msg, clear_chat_history
from utils.sql_api_utils import tuple_to_azure_message
from utils.text_to_speech import text_to_speech
# import streamlit_js_eval

# @st.cache_resource
def getAzureopenAI():
    azureOpenAI = AzureOpenAI()
    return azureOpenAI

def syncMessagesWithDB(messages: list):
    for message in messages:
        role = message['role']
        content = message['content'][0]['text']
        save_msg(chatTopic, role, content)
    return True

def fetchMessagesFromDB(chatTopic):
    chat_history = load_chat_history(chatTopic)
    messages = []
    for entry in chat_history:
        messages.append(tuple_to_azure_message(entry))
    return messages

def generate_and_store_tts(text):
    audio_path = text_to_speech(text)
    return audio_path

def response_generator(prompt, azureOpenAI):
    response = azureOpenAI.generate_response_gpt4om(prompt)
    return response  # Return the response for tts

st.set_page_config(
    page_title="Chatbot",
    page_icon="👋",
)

# this is for initialize session state for messages if it does not exist
if 'messages' not in st.session_state:
    st.session_state.messages = []


chatTopic = sidebar("main")
azureOpenAI = getAzureopenAI() 


if chatTopic:
    # Load chat history for the selected session
    st.session_state.messages = fetchMessagesFromDB(chatTopic) 
    azureOpenAI.update_chat_history(st.session_state.messages) 
    st.title(f"Chat Session: {chatTopic}")
    
    #Remove system message
    if st.session_state.messages and st.session_state.messages[0]['role'] == 'system':
        st.session_state.messages.pop(0)

if chatTopic == "":
    st.title(f"Welcome to Info Prof!")
    st.text(f"To get started, create a new chat session on your left!")
    st.text(f"Alternatively, pick up where you left off by selecting a previous chat session!")

# Display chat messages from history
if st.session_state.messages:
    for index, message in enumerate(st.session_state.messages):
        message_content = message["content"][0]['text']
        with st.chat_message(message["role"]):
            col1, col2 = st.columns([9, 1])
            with col1:
                st.markdown(message_content)
            with col2:
                if st.button(label="Play TTS", key=f'play-{index}', use_container_width=True):
                    audio_file = text_to_speech(message_content)  # Converting text to speech
                    st.audio(audio_file, format="audio/mp3", start_time=0)  #This is for playing audio
                    os.remove(audio_file)  # Delete the audio file after playback

if chatTopic != "" and st.button("Clear Chat History"):
    print(chatTopic)
    clear_chat_history(chatTopic)  
    st.session_state.messages = []  # This is for clearing session state messages
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
    
    # Generate assistant response
    response = response_generator(prompt, azureOpenAI=azureOpenAI)
    
    # Display assistant's response
    with st.chat_message("assistant"):
        st.markdown(response)
    
    # Add assistant response to chat history
    assistant_message = {
        'role': 'assistant',
        'content': [{"type": "text", "text": response}]
    }

    # Append both user and assistant messages to the chat history in session state
    st.session_state.messages.append(user_message)
    st.session_state.messages.append(assistant_message)

    
    audio_file = text_to_speech(response) #this is for converting text to speech
    st.audio(audio_file, format="audio/mp3", start_time=0) #This is for playing audio
    os.remove(audio_file)   # Delete the audio file after playback


    syncMessagesWithDB([user_message, assistant_message])

    # print("azure ", len(azureOpenAI.get_chat_history()))
    # print('db: ', len(load_chat_history(chatTopic)))
    # print(load_chat_history(chatTopic))

