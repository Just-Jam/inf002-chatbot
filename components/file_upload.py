import streamlit as st

def file_upload():
    if 'uploaded_file' not in st.session_state:
        st.session_state.uploaded_file = None  # Stores the content of the uploaded file

    if 'file_uploaded_message_shown' not in st.session_state:
        st.session_state.file_uploaded_message_shown = False  # Flag to show upload message only once

        # File Upload
    uploaded_file = st.file_uploader("Upload a text file", type=["txt", "pdf"])  # Allow user to upload a text file

    if uploaded_file is not None:
        st.session_state.uploaded_file = uploaded_file.read().decode('utf-8')  # Read and decode the uploaded file

    # Show upload message only once
    if not st.session_state.file_uploaded_message_shown:
        # st.session_state.history.append(
        #     "File uploaded successfully. What do you want to do with the file?"
        # )
        st.markdown("File uploaded successfully. What do you want to do with the file?",unsafe_allow_html=True)
        st.session_state.file_uploaded_message_shown = True  # Set flag to true after showing the message

        # # Check if a file is uploaded first
        if st.session_state.uploaded_file:
            # Process user request related to the uploaded file
            file_content = st.session_state.uploaded_file
        #     if 'summarize' in usrinput.lower():
        #         query = f"Summarize the following text: {file_content}"  # Create summary query
        #     elif 'analyze' in usrinput.lower():
        #         query = f"Analyze the following text: {file_content}"  # Create analysis query
        #     else:
        #         query = f"{usrinput}: {file_content}"  # General query with user input and file content
        # else:
        #     # If no file is uploaded, just respond to general chat
        #     query = usrinput  # Use the user input directly