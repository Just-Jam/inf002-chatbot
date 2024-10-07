import streamlit as st
from database.database import get_sessions, save_msg
from api.azure import AzureOpenAI
import time
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
        print(">>>>>>>>>>>>>>",id)
        save_msg(chatTopic, role, content, id)
    return True

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

def sidebar(group_id):
    st.sidebar.title("Previous chat topics")
    
    # Get all existing chat sessions
    sessions = get_sessions(group_id)

    # Create a selectbox for existing sessions or a "New Chat" option
    session_selection = st.sidebar.selectbox("Select a session", ["Select chat topics"] + sessions)
    
    if session_selection == "Select chat topics":
        chatTopic = st.sidebar.text_input("Enter new session name:", key="new_session", placeholder="Enter chat topic")

        if chatTopic and chatTopic not in sessions:
            st.sidebar.success(f"New chat session '{chatTopic}' created.")
            azureOpenAI = AzureOpenAI()
            
            
            syncMessagesWithDB([user_msg("Hello"), assistant_msg(st.write_stream(response_generator("Hello", azureOpenAI=azureOpenAI)))], chatTopic)
            st.rerun()
    else:
        chatTopic = session_selection
        st.sidebar.info(f"Selected session: {chatTopic}")

    return chatTopic
