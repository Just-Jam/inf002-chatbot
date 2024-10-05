import streamlit as st
from database import validate_user

# Sample user data (you can replace this with a database query)
USER_DATA = {
    "user1": "password1",
    "user2": "password2"
}

# Function to check login


def display_login_form():
    st.title("Login")
    email = st.text_input("Email Address")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        user = validate_user(email, password)
        if user:
            st.success(f"Welcome {user[1]}!")
            st.session_state['username'] = user[1]  # Save user_id to session state for future use
            # Redirect to main.py or show chat UI here
            st.switch_page("main.py")

        else:
            st.error("Invalid email or password. Please try again.")
    if st.button("Register"):
        st.switch_page("pages\Registration.py")

# Call this function to display the form
display_login_form()
