import streamlit as st
import regex as re
from database import register_user
email = st.text_input("Email Address", key="email", placeholder="Enter your email")
username = st.text_input("Username", key="username", placeholder="Choose a username")
password = st.text_input("Password", type="password", key="password", placeholder="Create a password")
cfmPassword = st.text_input("Confirm Password", type="password", key="cfmPassword", placeholder="Confirm your password")

# Validate email format
def is_valid_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

# Validate password
def validate_password(password, cfmPassword):
    if len(password) < 6:
        return False, "Password must be at least 6 characters long."
    if password != cfmPassword:
        return False, "Passwords do not match."
    return True, None

# Submit button
if st.button("Register", key="register-button", help="Click to register"):
    if not is_valid_email(email):
        st.error("Invalid email address")
    else:
        valid, error_msg = validate_password(password, cfmPassword)
        if not valid:
            st.error(error_msg)
        else:
            register_user(username, email, password)
            st.success(f"Registration successful! Welcome, {username}!")
            st.switch_page("pages\Login.py")
