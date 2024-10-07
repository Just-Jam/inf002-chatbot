import streamlit as st
import time
import uuid
from api.azure import AzureOpenAI
from components.sidebar import sidebar
from database.database import load_chat_history, save_msg, clear_chat_history
from utils.sql_api_utils import tuple_to_azure_message
import pymupdf  # PyMuPDF for handling PDF files
from docx import Document # Document class from the python-docx library
from menu import menu

# Function to handle .txt files
def extract_text_from_txt(file):
    """Extract text from a plain text (.txt) file"""
    return file.read().decode('utf-8')

# Function to handle .docx files
def extract_text_from_docx(file):
    """Extract text from a DOCX file using python-docx"""
    doc = Document(file)
    full_text = []
    for paragraph in doc.paragraphs:
        full_text.append(paragraph.text)
    return '\n'.join(full_text)

# Function to handle .pdf files
def extract_text_from_pdf(file):
    """Extract text from a PDF file using PyMuPDF (fitz)"""
    pdf_document = pymupdf.open(stream=file.read(), filetype="pdf")
    text = ""
    for page_num in range(len(pdf_document)):
        page = pdf_document.load_page(page_num)
        text += page.get_text()
    pdf_document.close()
    return text

# Function to handle file uploads
def handle_file_upload(uploaded_file):
    """Extract text from uploaded files based on their type."""
    # Mapping file types to respective extraction functions
    file_type_handlers = {
        "text/plain": extract_text_from_txt,  # Handler for .txt files
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document": extract_text_from_docx,  # Handler for .docx files
        "application/pdf": extract_text_from_pdf,  # Handler for .pdf files
    }
    
    # Get the appropriate handler function based on the uploaded file type
    handler = file_type_handlers.get(uploaded_file.type)
    
    if handler:
        try:
            # Use the handler function to extract text from the uploaded file
            return handler(uploaded_file)
        except Exception as e:
            # Show an error message if there is an issue during file processing
            st.error(f"Error processing file: {e}")
    else:
        # If the file type is unsupported, notify the user
        st.error("Unsupported file type. Please upload a .txt, .docx, or .pdf file.")
    
    return None  # Return None if no valid handler was found or an error occurred


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
    st.rerun()


st.set_page_config(
    page_title="File Assistant",
    page_icon="👋",
)
menu()


GROUP_ID = "file_assistant"
chatTopic = sidebar(GROUP_ID)
azureOpenAI = getAzureopenAI()
messages = []
summarize_btn = None

#file upload UI
if 'uploaded_file' not in st.session_state:
    st.session_state.uploaded_file_content = None  # Stores the content of the uploaded file

if 'file_uploaded_message_shown' not in st.session_state:
    st.session_state.file_uploaded_message_shown = False  # Flag to show upload message only once

# File Upload
uploaded_file = st.file_uploader("Upload a text file", type=["txt", "docx", "pdf"])  # Allow user to upload a text file

if uploaded_file:
    # Call the handle_file_upload function to extract text
    st.session_state.uploaded_file_content = handle_file_upload(uploaded_file)

    # Show upload message only once
    if st.session_state.uploaded_file_content and not st.session_state.file_uploaded_message_shown:
        st.markdown("File uploaded successfully. What do you want to do with the file?", unsafe_allow_html=True)
        st.session_state.file_uploaded_message_shown = True

    # Provide options to summarize
    summarize_btn = st.button("Summarize")

    if st.button("Test"):
        azureOpenAI.generate_embeddings(st.session_state.uploaded_file_content)


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
    st.rerun()

if summarize_btn:
    summarize_text(st.session_state.uploaded_file_content)

