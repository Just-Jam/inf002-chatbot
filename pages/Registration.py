import streamlit as st
from menu import menu

def RegisterPage():
    auth = menu()
    auth.registration_widget()

if __name__ == '__main__':
    RegisterPage()

