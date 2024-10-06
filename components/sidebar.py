import streamlit as st
from database.database import get_sessions

def sidebar(group_id):
    st.sidebar.title("Previous chat topics")
    
    # Get all existing chat sessions
    sessions = get_sessions(group_id)

    # Create a selectbox for existing sessions or a "New Chat" option
    session_selection = st.sidebar.selectbox("Select a session", ["Select chat topics"] + sessions)
    
    if session_selection == "Select chat topics":
        chatTopic = st.sidebar.text_input("Enter new session name:", key="new_session", placeholder="Enter chat topic")

        if chatTopic:
            st.sidebar.success(f"New chat session '{chatTopic}' created.")
    else:
        chatTopic = session_selection
        st.sidebar.info(f"Selected session: {chatTopic}")

    return chatTopic
