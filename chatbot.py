import streamlit as st
import os
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
from langchain_google_genai import GoogleGenerativeAI
import time


# Load environment variables (API keys)
load_dotenv()

# Set page title and icon for Streamlit
st.set_page_config(page_title="Chat with Gemini", page_icon="🤖")

# Sidebar configuration
with st.sidebar:
    st.title("Chat Settings")
    select_model = st.selectbox(
        "Choose a Gemini Model:",
        ["gemini-1.5-pro-latest", "gemini-1.0-pro", "gemini-1.0-pro-vision"]
    )
    st.write("Select a model to interact with Chatrr!")

# Initialize memory for the conversation
if "conversation_history" not in st.session_state:
    st.session_state.conversation_history = []

# Streamlit UI for conversation
st.title("Chat with Chattr")
st.markdown("### Ask me anything below:")

llm = GoogleGenerativeAI(
    model=select_model , # Specify the model you want to use
    google_api_key=os.getenv("GOOGLE_API_KEY")  # Ensure your API key is set in the environment
)

         # Use ConversationBufferMemory to retain chat context across interactions
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
user_input = st.text_area("Type your question here...", height=150, placeholder="Ask something...")

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


