import streamlit as st
from utils.user_auth import UserAuth
import streamlit_authenticator as stauth

def menu():
    #Auth: auto login on load
    auth = UserAuth()
    st.session_state['authenticator'] = auth.get_authenticator()
    try:
        st.session_state['authenticator'].login(location='unrendered')
    except stauth.LoginError as e:
        st.error(e)

    if st.session_state['authentication_status'] is None or False:
        st.sidebar.page_link("pages/Login.py", label="Log in")
        st.sidebar.page_link("pages/Registration.py", label="Register")
    else:
        with st.sidebar:
            st.write(f"Logged in as {st.session_state['username']}")
    st.sidebar.page_link("main.py", label="Home")
    st.sidebar.page_link("pages/3_File Assistant.py", label="File Assistant")
    st.sidebar.page_link("pages/4_Image Generator.py", label="Image Generator")

    # st.sidebar.button("Logout")
    if st.session_state['authentication_status']:
        with st.sidebar:
            auth.authenticator.logout()

    return auth