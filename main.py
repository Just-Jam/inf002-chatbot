import streamlit as st
import time
import os
from api.azure import AzureOpenAI
from menu import menu
from components.authenticated_chat import authenticated_chat

def response_generator(prompt, azureOpenAI):
    response = azureOpenAI.generate_response_gpt4om(prompt)
    for word in response.split():
        yield word + " "
        time.sleep(0.05)

def guest_chat(azureOpenAI):
    st.title("Welcome to chatbot")
    # Initialize chat history
    if "guest_messages" not in st.session_state:
        st.session_state.guest_messages = []

    # Display chat messages from history on app rerun
    for message in st.session_state.guest_messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Accept user input
    if prompt := st.chat_input("What is up?"):
        # Add user message to chat history
        st.session_state.guest_messages.append({"role": "user", "content": prompt})
        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(prompt)

        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            response = st.write_stream(response_generator(prompt, azureOpenAI))
        # Add assistant response to chat history
        st.session_state.guest_messages.append({"role": "assistant", "content": response})

def main():
    st.set_page_config(
        page_title="Chatbot",
        page_icon="👋",
    )

    menu()
    azureOpenAI = AzureOpenAI()
    chatTopic = ""

    #Guest chat logic
    if st.session_state['authentication_status'] is None or False:
        guest_chat(azureOpenAI)

    #User is authenticated
    else:
        st.title(f"Welcome back {st.session_state['username']}!")
        st.text(f"To get started, create a new chat session on your left!")
        st.text(f"Alternatively, pick up where you left off by selecting a previous chat session!")

        authenticated_chat(azureOpenAI)


if __name__ == '__main__':
    main()