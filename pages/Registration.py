import streamlit as st
from utils.user_auth import UserAuth

def RegisterPage():
    auth = UserAuth()
    auth.registration_widget()

if __name__ == '__main__':
    RegisterPage()

