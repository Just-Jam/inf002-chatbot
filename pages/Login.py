import streamlit as st
from menu import menu

def LoginPage():
    auth = menu()
    auth.login_widget()
    st.page_link("pages/Registration.py", label="Register")
    if st.session_state['authentication_status']:
        st.write(f'Welcome *{st.session_state["name"]}*')
        st.switch_page('main.py')

if __name__ == '__main__':
    LoginPage()
