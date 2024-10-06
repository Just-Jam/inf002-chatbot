import streamlit as st
from utils.user_auth import UserAuth

def LoginPage():
    auth = UserAuth()
    auth.login_widget()
    st.page_link("pages/Registration.py", label="Register")
    if st.session_state['authentication_status']:
        auth.authenticator.logout()
        st.write(f'Welcome *{st.session_state["name"]}*')
        st.title('Some content')
        # st.switch_page('main.py')

if __name__ == '__main__':
    LoginPage()
