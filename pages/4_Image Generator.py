import streamlit as st
import time
from api.azure import AzureOpenAI
from menu import menu

st.set_page_config(
    page_title="Image Generator",
    page_icon="👋",
)

menu()

prompt = st.text_area(label="What kind of image do you want to generate?")
generate_btn = st.button("Generate Image")
azureOpenAI = AzureOpenAI()

if generate_btn:
    with st.spinner('Generating Image...'):
        image_path = azureOpenAI.generate_image_dalle3(prompt)
    st.image(image_path, caption=prompt)

