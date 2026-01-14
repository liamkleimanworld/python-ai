from dotenv import load_dotenv
import os
import streamlit as st
from google import genai

all_models = ["gemini-2.5-flash",
              "gemini-2.0-flash",
              "gemini-2.5-flash-lite",
              "gemini-2.0-flash-lite"]




def createClient():
    st.session_state.client = genai.Client(api_key=loadAPIKey())

def sendMessage(text,history = []):
    if 'client' not in st.session_state:
        createClient()

    for model in all_models:
        client = st.session_state.client
        try:
            chat = client.chats.create(
                model = model,
                history = history
            )
            ai = chat.send_message(text)
            print(ai.text)
        except Exception as e:
            error = str(e)
            if "429" in error:
                st.error("you messaged the chat too many messages, please try again later")
                return
            if "503" in error:
                st.info(f"the model is not available, try other models")
            else:
                st.info("Error: "+error)
                return
            print (f"{model} not working...")

def loadAPIKey():
    load_dotenv()
    API_KEY = os.getenv("API_KEY") or st.secrets["API_KEY"]
    return API_KEY

def showMessage (sender,text):
    newMessage = st.chat_message(sender)
    newMessage.write(text)


def save_to_history(project,sender,text):
    if project not in st.session_state:
        st.session_state[project] = {
            "history":[]
        }
        st.session_state[project]["history"].append(
            {
            "role" : sender,
            "parts" : text
        }
        )

