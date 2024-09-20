import json
import streamlit as st
import time
from api.azure import generate_response_gpt4om

# styling the messages, should rename function name to style_user_message
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

# can rename to style_bot_message
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
def main():
    if 'history' not in st.session_state:
        st.session_state.history = []


    st.markdown("""
        <style>
        @keyframes float-up {
            0% { transform: translateY(30px); opacity: 0; }
            100% { transform: translateY(0); opacity: 1; }
        }
        </style>
        """, unsafe_allow_html=True)

    for msg in st.session_state.history:
        st.markdown(msg, unsafe_allow_html=True)

    if usrinput := st.chat_input("🤖Ask me anything here:"):
        # Hard coded bot response vvvvvvvvv
        st.session_state.history.append(prompt(usrinput))
        st.markdown(prompt(usrinput), unsafe_allow_html=True) # this line doesnt do anything?

        response = generate_response_gpt4om(usrinput)
        st.session_state.history.append(bot_message(response))
        st.markdown(bot_message(response), unsafe_allow_html=True) # this line doesnt do anything?
        st.rerun()

        # Dynamic bot response vvvvvvvvv (not yet working)

        # st.session_state.history.append(prompt(usrinput))
        # st.session_state.messages.append({"role": "user", "content": usrinput})
        # with st.chat_message("user"):
        #     st.markdown(prompt)

        # with st.chat_message("assistant"):
        #     stream = client.chat.completions.create(
        #         model=st.session_state["openai_model"],
        #         messages=[
        #             {"role": m["role"], "content": m["content"]}
        #             for m in st.session_state.messages
        #         ],
        #         stream=True,
        #     )
        #     response = st.write_stream(stream)
        # st.session_state.messages.append({"role": "assistant", "content": response})

        st.markdown(prompt(usrinput), unsafe_allow_html=True)
        response = "Hello there!"
        st.markdown(bot_message(response), unsafe_allow_html=True)
        st.rerun()

    if len(st.session_state.history) > 0 and 'bot_replied' not in st.session_state:
        # Delay bot response by 2 seconds
        time.sleep(1)
        bot_reply = "I'm just a bot!"
        st.session_state.history.append(bot_message(bot_reply))
        st.session_state.bot_replied = True

        # Rerun the app to display the bot response after the delay
        st.rerun()

if __name__ == '__main__':
    main()



