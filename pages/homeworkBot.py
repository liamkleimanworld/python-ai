import streamlit as st
from helper import*


st.set_page_config(
    page_title= "Homework Bot" ,
    page_icon="🤓"
)

st.title("homwork bot")


api_key = loadAPIKey()
#the first message from the chat
showMessage("AI","I am here to help you with your work")

#place to tipe
user = st.chat_input("Write something…")

#if there is a message
if user:
    showMessage ("user",user)