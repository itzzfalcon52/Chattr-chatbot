import streamlit as st
import os
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
from langchain_google_genai import GoogleGenerativeAI
import time

st.set_page_config(page_title="Chat with Gemini", page_icon="🤖")

# Custom CSS for Streamlit UI styling
st.markdown("""
    <style>
        /* Overall page background and text */
        body, .stApp {
            background-color: #000000; /* Pure black background */
            color: #00ff41; /* Matrix green text color */
            font-family: 'Courier New', monospace; /* Hacker-style font */
        }

        /* Sidebar background */
        section[data-testid="stSidebar"] {
            background-color: #0d0d0d; /* Dark gray sidebar */
        }

        /* Titles: h1, h2, h3 */
        h1, h2, h3 {
            color: #00ff41; /* Titles in green */
        }

        /* Text input fields (textbox, textarea) */
        textarea, input {
            background-color: #1a1a1a; /* Slightly lighter black */
            color: #00ff41; /* Green text inside input */
            border: 1px solid #00ff41; /* Green border */
            border-radius: 8px; /* Smooth rounded corners */
            padding: 10px; /* Space inside the box */
        }

        /* Main chat button styling */
        .stButton > button {
            background-color: #00ff41; /* Green button */
            color: #000000; /* Black text on button */
            font-weight: bold; /* Make button text bold */
            font-size: 16px; /* Bigger button text */
            padding: 10px 20px; /* Button padding */
            border: none; /* No default border */
            border-radius: 10px; /* Rounded button shape */
            transition: 0.3s; /* Smooth hover animation */
        }

        /* Button hover effect */
        .stButton > button:hover {
            background-color: #00cc34; /* Slightly darker green on hover */
            transform: scale(1.02); /* Button grows slightly on hover */
        }

        /* Chat message bubbles (general) */
        div.stChatMessage {
            background-color: #0d0d0d; /* Dark bubble background */
            padding: 1rem; /* Bubble padding */
            margin-bottom: 0.5rem; /* Space between bubbles */
            border-radius: 1rem; /* Rounded bubbles */
            border: 1px solid #00ff41; /* Green border for messages */
        }

        /* User chat messages */
        div.stChatMessage.user {
            background-color: #1a1a1a; /* Slightly lighter background for user */
            border-left: 4px solid #00ff41; /* Green bar on the left */
        }

        /* Assistant (bot) chat messages */
        div.stChatMessage.assistant {
            background-color: #141414; /* Even darker background for assistant */
            border-left: 4px solid #00cc34; /* Darker green bar for assistant */
        }
    </style>
""", unsafe_allow_html=True)

GOOGLE_API_KEY = "AIzaSyB64GZ8RJsj8WE44SOnyKG36hAk7yXPrVY"  


# Sidebar configuration
with st.sidebar:
    st.title("Chat Settings")
    select_model = st.selectbox(
        "Choose a Gemini Model:",
        ["gemini-1.5-pro-latest", "gemini-1.0-pro", "gemini-1.0-pro-vision"]
    )
    st.write("Select a model to interact with Chattr!")


if "conversation_history" not in st.session_state:
    st.session_state.conversation_history = []

# Streamlit UI for conversation
st.title("Chat with Chattr")
st.markdown("### Ask me anything below:")

llm = GoogleGenerativeAI(
    model=select_model, 
    google_api_key=GOOGLE_API_KEY  
)


if "memory" not in st.session_state:
    st.session_state.memory = ConversationBufferMemory(memory_key="history", return_messages=True)

if "conversation" not in st.session_state:
    st.session_state.conversation = ConversationChain(
        llm=llm,
        memory=st.session_state.memory,
        verbose=True
    )

for msg in st.session_state.memory.chat_memory.messages:
    if msg.type == "human":
        with st.chat_message("user"):
            st.markdown(msg.content)
    elif msg.type == "ai":
        with st.chat_message("assistant"):
            st.markdown(msg.content)

# User input
user_input = st.text_area("Type your question here...", height=150, placeholder="Ask something...", key="user_input")

# Button to submit question
if st.button("Ask Chattr"):
    if user_input:
        # Display user message immediately
        with st.chat_message("user"):
            st.markdown(user_input)

        # Run the conversation chain with memory
        with st.spinner("Chattr is thinking..."):
            progress = st.progress(0)
            for i in range(100):
                time.sleep(0.05)
                progress.progress(i + 1)
            response = st.session_state.conversation.predict(input=user_input)

        # Display bot response
        with st.chat_message("assistant"):
            st.markdown(response)
    else:
        st.error("Please enter a question to ask Chattr!")
