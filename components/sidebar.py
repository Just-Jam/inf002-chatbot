import streamlit as st
from database.database import get_sessions, save_msg, get_all_sessions
from api.azure import AzureOpenAI
import time

DEFAULT_SYS_MESSAGE: str = "You are an AI assistant that helps people find information."

def response_generator(prompt, azureOpenAI):
    response = azureOpenAI.generate_response_gpt4om(prompt)
    for word in response.split():
        yield word + " "
        time.sleep(0.05)

def syncMessagesWithDB(messages: list, chatTopic):
    for message in messages:
        role = message['role']
        content = message['content'][0]['text']
        id = st.session_state['username']
        if id == None:
            id = "main"
        save_msg(chatTopic, role, content, id)
    return True

def user_msg(prompt):
    return {
        'role': 'user',
        'content': [{"type": "text", "text": prompt}]
    }

def assistant_msg(response):
    return {
        'role': 'assistant',
        'content': [{"type": "text", "text": response}]
    }

def create_new_session(chatTopic):
    system_message = {
        "role": "system",
        "content": [{"type": "text", "text": DEFAULT_SYS_MESSAGE}]
    }
    syncMessagesWithDB([system_message], chatTopic)

def sidebar(group_id):
    st.sidebar.title("Previous chat topics")
    
    # Get all existing chat sessions
    sessions = get_sessions(group_id)

    # Map to store the displayed topic (without username) and the actual session value
    display_to_session_map = {}
    
    # Populate the dictionary, showing the clean name but keeping the full chat session
    for session in sessions:
        chat_topic_only = session.split(":")[0]
        if chat_topic_only not in display_to_session_map:
            display_to_session_map[chat_topic_only] = session

    # Create a selectbox for existing sessions or a "New Chat" option
    session_display_list = ["Select chat topics"] + list(display_to_session_map.keys())
    session_selection = st.sidebar.selectbox("Select a session", session_display_list)

    if session_selection == "Select chat topics":
        chatTopic = st.sidebar.text_input("Enter new session name:", key="new_session", placeholder="Enter chat topic")
        
        chatlist = get_all_sessions()
        if chatTopic in chatlist:
            chatTopic = chatTopic + ":" + group_id
        
        if chatTopic and chatTopic not in sessions:
            st.sidebar.success(f"New chat session '{chatTopic}' created.")
            create_new_session(chatTopic)
            st.rerun()

    else:
        # Get the full session name (with username) from the map
        chatTopic = display_to_session_map[session_selection]
        st.sidebar.info(f"Selected session: {chatTopic}")

    return chatTopic
