from dotenv import load_dotenv
import os
import streamlit as st

def loadAPIKey():
    load_dotenv()
    API_KEY = os.getenv("API_KEY") or st.secrets["API_KEY"]
    return API_KEY

def showMessage (sender,text):
    newMessage = st.chat_message(sender)
    newMessage.write(text)