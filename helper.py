from dotenv import load_dotenv
import os
import streamlit as st
from google import genai

all_models = ["gemini-3-flash",
              "gemini-2.5-flash",
              "gemini-2.0-flash",
              "gemini-2.5-flash-lite",
              "gemini-2.0-flash-lite"]




def createClient():
    st.session_state.client = genai.client(api_key=loadAPIKey())

def sendMessage(text,history):
    if 'client' not in st.session_state:
        createClient()

    for model in all_models:
        client = st.session_state.client
        try:
            chat = client.chat(
                model = model
            )
        except:
            print (f"{model} not working...")

def loadAPIKey():
    load_dotenv()
    API_KEY = os.getenv("API_KEY") or st.secrets["API_KEY"]
    return API_KEY

def showMessage (sender,text):
    newMessage = st.chat_message(sender)
    newMessage.write(text)