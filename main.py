import streamlit as st
import time
import os
from api.azure import AzureOpenAI
from components.sidebar import sidebar
from database.database import load_chat_history, save_msg, clear_chat_history
from utils.sql_api_utils import tuple_to_azure_message
from utils.text_to_speech import text_to_speech
from menu import menu

def syncMessagesWithDB(messages: list, chatTopic):
    for message in messages:
        role = message['role']
        content = message['content'][0]['text']
        id = st.session_state['username']
        if id == None:
            id = "main"
        print(">>>>>>>>>>>>>>",id)
        save_msg(chatTopic, role, content, id)
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

def main():
    st.set_page_config(
        page_title="Chatbot",
        page_icon="👋",
    )

    menu()
    messages = []
    azureOpenAI = AzureOpenAI()
    chatTopic = ""
    
    if st.session_state['authentication_status'] is None or False:
        st.title(f"Welcome to Info Prof!")
        st.text(f"To get started, create a new chat session on your left!")
        st.text(f"Alternatively, pick up where you left off by selecting a previous chat session!")
    else:
        st.title(f"Welcome back {st.session_state['username']}!")
        chatTopic = sidebar(st.session_state['username'])
    
        if chatTopic:
            print("Chattopic: ", chatTopic)
            # Load chat history for the selected session
            messages = fetchMessagesFromDB(chatTopic)
            azureOpenAI.update_chat_history(messages)
            #st.title(f"Chat Session: {chatTopic}")
            # Remove system message
            messages.pop(0)
        # elif 'username' in st.session_state:
        #     user_id = st.session_state['username']
        #     st.title(f"Welcome Back {user_id}!")
        if chatTopic != "" and st.button("Clear Chat History"):
            clear_chat_history(chatTopic)
            time.sleep(2)
            st.success("History Cleared!")
            st.rerun()
            # streamlit_js_eval(js_expressions="parent.window.location.reload()")

    # Display chat messages from history
    for index, message in enumerate(messages):
        message_content = message["content"][0]['text']
        with st.chat_message(message["role"]):
            col1, col2 = st.columns([9, 1])
            with col1:
                st.markdown(message_content)
            with col2:
                if st.button(label="Play TTS", key=f'play-{index}', use_container_width=True):
                    print("hello")
                    audio_file = text_to_speech(message_content)  # Converting text to speech
                    st.audio(audio_file, format="audio/mp3", start_time=0)  # This is for playing audio
                    os.remove(audio_file)  # Delete the audio file after playbacke audio file after playback

    

    # Accept user input
    if prompt := st.chat_input("What is up?"):
        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(prompt)
        # Add user message to chat history
        
        

        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            response = st.write_stream(response_generator(prompt, azureOpenAI=azureOpenAI))
        # Add assistant response to chat history
        
        assistant_msg(response)
        syncMessagesWithDB([user_msg(prompt), assistant_msg(response)], chatTopic)
        #st.rerun()


def user_msg(prompt):
    user_message = {
            'role': 'user',
            'content': [{"type": "text", "text": prompt}]
        }
    return user_message

def assistant_msg(response):
    assistant_message = {
            'role': 'assistant',
            'content': [{"type": "text", "text": response}]
        }
    return assistant_message





if __name__ == '__main__':
    main()