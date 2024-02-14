# Boilerplate code - Setting up streamlit on Gemini Pro model

# import all dependencies
import vertexai
import streamlit as st
from vertexai import init, preview
from vertexai.preview import generative_models
from vertexai.preview.generative_models import GenerativeModel, GenerationConfig, Part, Content, ChatSession

#setup - Initialize Vertex AI with your project ID

# message = st.chat_message("assistant")


init(project = "gemini-explorer-413607")

config = GenerationConfig(
    temperature = 0.4
)

# load model with config

model = GenerativeModel(
    "gemini-pro",
    generation_config = config
)

# Start the chat session
chat = model.start_chat()

# helper function to display and send streamlit messages

def llm_function(chat: ChatSession, query):
   response = chat.send_message(query)
   output = response.candidates[0].content.parts[0].text

   with st.chat_message("model"):
      st.markdown(output)
   
   st.session_state.message.append(
      {
         "role":"user",
         "content": query,
      }
   )

   st.session_state.message.append(
      {
         "role":"model",
         "content": output,
      }
   )
   
   
   # Streamlit UI
   st.title("Gemini Explorer Chat")

# Initialize chat session
if "message" not in st.session_state:
      st.session_state.message = []

# Display and load chat history
      
   # Initialize chat session
if "message" not in st.session_state:
    st.session_state.message = []

# Display and load chat history
for index, message in enumerate(st.session_state.message):
    content = Content(
        role=message["role"],
        parts=[Part.from_text(message["content"])]  # Corrected the syntax here
    )
    with st.chat_message(message["role"]):  # Used the correct role variable here
        st.markdown(message["content"])
    chat.history.append(content)

# Step 1: Add Initial Message Logic
if len(st.session_state.message) == 0:
    initial_prompt = "Introduce yourself as Rex..."   
    llm_function(chat, initial_prompt)

# For capture user input
query = st.chat_input("Gemini Explorer")   

if query:
   with st.chat_message("user"):
       st.markdown(query)
   llm_function (chat, query)    

