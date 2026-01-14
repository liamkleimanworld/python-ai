import streamlit as st
from helper import*


st.set_page_config(
    page_title= "Homework Bot" ,
    page_icon="🤓"
)

st.title("homework bot")


api_key = loadAPIKey()
#the first message from the chat
showMessage("AI","I am here to help you with your work")

#place to tipe
user = st.chat_input("Write something…")

#if there is a message
if user:
    showMessage ("user",user)
    save_to_history("homework","user",user)
    history = st.session_state["homework"]["history"]
    answer = sendMessage(user)
    showMessage ("ai",answer)


    save_to_history("homework","model",answer)

