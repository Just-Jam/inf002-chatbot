import streamlit as st
import time
from api.azure import AzureOpenAI
from database import save_msg, load_chat_history, clear_chat_history
from streamlit_js_eval import streamlit_js_eval
from sidebar import sidebar
import uuid
from stylings import promptStyle, botMessageStyle

# styling the messages, should rename function name to style_user_message


chatTopic = sidebar()
if chatTopic:
    # Load chat history for the selected session
    chat_history = load_chat_history(chatTopic)
    st.title(f"Chat Session: {chatTopic}")
    for sender, message in chat_history:

        if sender == "user":
            st.markdown(promptStyle(message), unsafe_allow_html=True)
        else:
            st.markdown(botMessageStyle(message), unsafe_allow_html=True)

    usrinput = st.chat_input("🤖Ask me anything here:")
    azureOpenAI = AzureOpenAI()

    if usrinput:
        # Hard coded bot response vvvvvvvvv
        usr_uuid = uuid.uuid4()
        save_msg(str(usr_uuid), chatTopic, "user", usrinput)
        response = azureOpenAI.generate_response_gpt4om(usrinput)
        time.sleep(1)
        bot_uuid = uuid.uuid4()
        save_msg(str(bot_uuid), chatTopic, "bot", response)
        st.rerun()

if chatTopic == "":
    st.title(f"Welcome to Info Prof!")
    st.text(f"To get started, create a new chat session on your left!")
    st.text(f"Alternatively, pick up where you left off by selscting a previous chat session!")

if chatTopic != "" and st.button("Clear Chat History"):
    print(chatTopic)
    clear_chat_history(chatTopic)
    st.success("Clearing history...")
    time.sleep(2)
    streamlit_js_eval(js_expressions="parent.window.location.reload()")

if 'history' not in st.session_state:
    st.session_state.history = []

# st.markdown("""
#     <style>
#     @keyframes float-up {
#         0% { transform: translateY(30px); opacity: 0; }
#         100% { transform: translateY(0); opacity: 1; }
#     }
#     </style>
#     """, unsafe_allow_html=True)

for msg in st.session_state.history:
    st.markdown(msg, unsafe_allow_html=True)


