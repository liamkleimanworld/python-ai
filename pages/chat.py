import os
from dotenv import load_dotenv
from google import genai
import streamlit as st

# --- Page Config MUST be first ---
st.set_page_config(
    page_title="chat with eminem",
    page_icon='😏',
    layout="wide"
)


# 🎨 Load CSS for UI
st.markdown("""
<style>
    .stApp {
        background: #0f172a;
        font-family: 'Poppins', sans-serif;
        color: white;
    }
    .main-title {
        font-size: 3.2rem;
        font-weight: 800;
        text-align: center;
        margin-top: -20px;
    }
    .sub-title {
        font-size: 1.3rem;
        text-align: center;
        opacity: 0.65;
        margin-bottom: 30px;
    }
    section[data-testid="stSidebar"] {
        background: #1e293b;
        border-right: 1px solid #334155;
    }
    .chat-container {
        border-radius: 16px;
        padding: 20px;
        background: #1e293b;
        min-height: 70vh;
        box-shadow: 0 4px 20px rgba(0,0,0,0.4);
    }
</style>
""", unsafe_allow_html=True)

# 🏷 Title Section
st.markdown('<div class="main-title">Chat with Slim Shady 🎤</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">AI that spits bars back at you 💬🔥</div>', unsafe_allow_html=True)

# 🧭 Sidebar Navigation
st.sidebar.markdown("## 🚀 Navigation")
page = st.sidebar.radio("", ["Chat", "About"])

# 🔑 Load Environment + API
load_dotenv()
API_KEY = os.getenv("API_KEY")
gemini = genai.Client(api_key=API_KEY)

# 🧠 Save chat history
def saveToHistory(sender, text):
    st.session_state.history.append({
        "sender": sender,
        "text": text
    })

# 📤 Send message through multiple models fallback
def send(prompt):
    saveToHistory("user", prompt)
    all_models = ["gemini-2.5-flash", "gemini-2.0-flash", "gemini-2.5-flash-lite", "gemini-2.0-flash-lite"]

    context = ""
    for line in st.session_state.history:
        context += f"{line['sender']} {line['text']}\n"

    for model in all_models:
        chat = st.session_state.gemini.chats.create(model=model)
        try:
            message = chat.send_message(prompt)
            saveToHistory("assistant", message.text)
            return message
        except:
            print(f"מודל {model} לא עבד - מנסה את הבא...")

# 🚦 Initialize session state
def start():
    st.session_state.gemini = genai.Client(api_key=API_KEY)
    st.session_state.history = []
    intro = """You answer like Eminem to everything you are asked.
    Answer the next question in rap style:
    Yo model, what's up?"""
    message = send(intro)

if "gemini" not in st.session_state:
    start()

# 💬 Main Page
if page == "Chat":
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)

    if 'history' in st.session_state:
        for line in st.session_state.history:
            user_chat = st.chat_message(line["sender"])
            user_chat.write(line["text"])

    st.markdown('</div>', unsafe_allow_html=True)

elif page == "About":
    st.markdown("### 🎤 Chat With Eminem AI")
    st.write("This bot answers everything like Eminem — ruthless, lyrical and full of bars.")

# 🎧 Chat input
prompt = st.chat_input("Write something…")

if prompt:
    user_msg = st.chat_message("user")
    user_msg.write(prompt)

    message = send(prompt)
    ai_msg = st.chat_message("assistant")
    ai_msg.write(message.text)
