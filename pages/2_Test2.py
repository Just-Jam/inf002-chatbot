import streamlit as st
from api.azure import AzureOpenAI
import pyttsx3

# Styling for user messages
def prompt(message):
    return f"""
       <div style="position: relative; background-color:#E1F5FE; padding:10px; border-radius:15px; margin-bottom:10px;
                   word-wrap: break-word;">
           <p style="color:#000; font-size:16px; margin:0;">You: {message}</p>
           <div style="position: absolute; top:10px; left:-10px; width:0; height:0; 
                       border-top:10px solid transparent; border-right: 10px solid #E1F5FE;
                       border-bottom:10px solid transparent;"></div>
       </div>
       """


# Styling for bot messages
def bot_message(message):
    return f"""
       <div style="position: relative; background-color:#C8E6C9; padding:10px; border-radius:15px; margin-bottom:10px;
                   word-wrap: break-word;">
           <p style="color:#000; font-size:16px; margin:0;">Bot: {message}</p>
           <div style="position: absolute; top:10px; right:-10px; width:0; height:0; 
                       border-top:10px solid transparent; border-left: 10px solid #C8E6C9;
                       border-bottom:10px solid transparent;"></div>
       </div>
       """


# this define function is meant for TTS
def speak_text(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()


def main():

    azureOpenAI = AzureOpenAI()

    if 'history' not in st.session_state:
        st.session_state.history = []  # Holds the chat history

    if 'uploaded_file' not in st.session_state:
        st.session_state.uploaded_file = None  # Stores the content of the uploaded file

    if 'file_uploaded_message_shown' not in st.session_state:
        st.session_state.file_uploaded_message_shown = False  # Flag to show upload message only once

    st.markdown("""
        <style>
        @keyframes float-up {
            0% { transform: translateY(30px); opacity: 0; }
            100% { transform: translateY(0); opacity: 1; }
        }
        </style>
        """, unsafe_allow_html=True)

    # Display the conversation history
    for msg in st.session_state.history:
        st.markdown(msg, unsafe_allow_html=True)  # Render each message in the chat history

    # If no user input, greet the user
    if len(st.session_state.history) == 0:
        bot_greeting = "Hello! How can I assist you today?"
        st.session_state.history.append(bot_message(bot_greeting))  # Append bot's greeting to history
        st.markdown(bot_message(bot_greeting), unsafe_allow_html=True)  # Display greeting in chat

    # File Upload
    uploaded_file = st.file_uploader("Upload a text file", type="txt")  # Allow user to upload a text file

    if uploaded_file is not None:
        st.session_state.uploaded_file = uploaded_file.read().decode('utf-8')  # Read and decode the uploaded file

        # Show upload message only once
        if not st.session_state.file_uploaded_message_shown:
            st.session_state.history.append(
                bot_message("File uploaded successfully. What do you want to do with the file?"))
            st.markdown(bot_message("File uploaded successfully. What do you want to do with the file?"),
                        unsafe_allow_html=True)
            st.session_state.file_uploaded_message_shown = True  # Set flag to true after showing the message

    # User input for file-based query or general chat
    if usrinput := st.chat_input("🤖Ask me anything here:"):
        st.session_state.history.append(prompt(usrinput))  # Append user message to history
        st.markdown(prompt(usrinput), unsafe_allow_html=True)  # Display user message in chat

        # Check if a file is uploaded first
        if st.session_state.uploaded_file:
            # Process user request related to the uploaded file
            file_content = st.session_state.uploaded_file
            if 'summarize' in usrinput.lower():
                query = f"Summarize the following text: {file_content}"  # Create summary query
            elif 'analyze' in usrinput.lower():
                query = f"Analyze the following text: {file_content}"  # Create analysis query
            else:
                query = f"{usrinput}: {file_content}"  # General query with user input and file content
        else:
            # If no file is uploaded, just respond to general chat
            query = usrinput  # Use the user input directly

        # Get response from the OpenAI/azure API
        response = azureOpenAI.generate_response_gpt4om(query)  # Call the API to get a response
        st.session_state.history.append(bot_message(response))  # Append bot response to history
        st.markdown(bot_message(response), unsafe_allow_html=True)  # Display bot response in chat

        speak_text(response)

        st.rerun()  # Rerun the app to update the display with new messages

    # Reset the flag if the user decides to upload a new file
    if uploaded_file is not None and usrinput and "upload" in usrinput.lower():
        st.session_state.uploaded_file = None  # Clear the uploaded file
        st.session_state.file_uploaded_message_shown = False  # Reset the message shown flag


if __name__ == '__main__':
    main()