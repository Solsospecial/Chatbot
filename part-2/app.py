import streamlit as st
from dotenv import load_dotenv
import os
import requests
# import speech_recognition as sr
import io

from pydantic_models import QueryRequest
from langchain_openai import ChatOpenAI
from langchain.agents import create_openai_tools_agent
from langchain.agents import AgentExecutor
from gpt_utils import *
from prompt import *
import pyttsx3 
import json
from pydub import AudioSegment
from pydub.playback import play
import simpleaudio as sa
import base64
# from deep_translator import GoogleTranslator

# Load environment variables
load_dotenv()

# Initialize Streamlit app
st.title("Streamlit Chatbot with PDF and Web Search")

"""
# Setup API Keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GOOGLE_CSE_ID = os.getenv("GOOGLE_CSE_ID")
"""

converter = pyttsx3.init()
converter.setProperty('rate', 150) 
# Set volume 0-1 
converter.setProperty('volume', 0.7) 

import requests

speech_url = "https://api.sarvam.ai/text-to-speech"
if "payload" not in st.session_state:
    st.session_state.payload = {
    "inputs": ["The weather is sunny."],
    "target_language_code": "hi-IN",
    "speaker": "meera",
    "pitch": 0,
    "pace": 1.65,
    "loudness": 1.5,
    "speech_sample_rate": 8000,
    "enable_preprocessing": True,
    "model": "bulbul:v1"
}
    st.session_state.headers = {
        "api-subscription-key": "3549d7f1-cbc8-49d5-bb04-0e0d5b778578",
        "Content-Type": "application/json"
    }


with st.sidebar:
    file_uploader = st.file_uploader("Upload your file:", type=["pdf"])
    url = st.text_input("Enter URL")
    if file_uploader is not None and "upload_pdf" not in st.session_state:
        response = requests.post(f"http://127.0.0.1:8000/add_pdf/", files={"file": file_uploader})
        if response.status_code == 200:
            st.success("Messages added successfully")
        st.session_state.upload_pdf = "positive"

    elif url and "url" not in st.session_state:
        if not url.startswith(('http://', 'https://')):
            st.error("Invalid URL format. Please ensure the URL starts with 'http://' or 'https://'.")
        else:
            response = requests.post(f"http://127.0.0.1:8000/scrape_webdata/", json={"url": url})
            if response.status_code == 200:
                st.success("Blog Extracted")
            else:
                st.error(f"Failed to add messages. Status code: {response.status_code}")
                st.error("Response content: " + response.text)
        st.session_state.url = "Positive"

if "pdf_search" not in st.session_state:
    st.session_state.pdf_tool = pdf_tool()

if "web_tool" not in st.session_state:
    st.session_state.web_tool = web_tool()

if "google_tool" not in st.session_state:
    st.session_state.google_tool = google_tool()

if "prompt" not in st.session_state:
    st.session_state.prompt = get_prompt()

def autoplay_audio(file_path: str):
    with open(file_path, "rb") as f:
        data = f.read()
    b64 = base64.b64encode(data).decode("utf-8")
    md = f"""
    <audio autoplay>
    <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
    </audio>
    """
    st.markdown(md, unsafe_allow_html=True)

# Create the LangChain agent
if "agent_executor" not in st.session_state:
    llm = ChatOpenAI(api_key=OPENAI_API_KEY)
    agent = create_openai_tools_agent(llm, [st.session_state.google_tool, st.session_state.pdf_tool, st.session_state.web_tool], st.session_state.prompt)
    st.session_state.agent_executor = AgentExecutor(agent=agent, tools=[st.session_state.google_tool, st.session_state.pdf_tool, st.session_state.web_tool], verbose=True, handle_parsing_errors=True, max_iterations=5)

# Streamlit interface
if "messages" not in st.session_state:
    st.session_state.messages = []
    with st.chat_message('assistant'):
        st.markdown("Hey Hii...! How can I help you.")
        st.session_state.payload["inputs"]=['Hey Hii...! How can I help you.']
        autoplay_audio('output.wav')

       


for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if len(st.session_state.messages)==0:
    st.session_state.messages.append({"role": "assistant", "content": "Hey Hii...! How can I help you."})


# Handle text input
if query := st.chat_input("Enter your query:"):
    st.session_state.messages.append({"role": "user", "content": query})
    with st.chat_message("user"):
        st.markdown(query)
    with st.spinner("Generating response..."):
        messages = st.session_state.messages
        messages_str = ""
        for message in messages:
            if message["role"] == "user":
                messages_str += f"User: {message['content']}///"
            elif message["role"] == "assistant":
                messages_str += f"Assistant: {message['content']}///"
        result = st.session_state.agent_executor.invoke({"input": query})
        st.markdown(result['output'])
        st.session_state.payload["inputs"]=[result['output']]
        response = requests.request("POST", speech_url, json=st.session_state.payload, headers=st.session_state.headers)

        print(response.text)
        json_data = json.loads(response.text)
        print(json_data)
        base64_string = json_data["audios"][0]
        # Decode the base64 string
        wav_data = base64.b64decode(base64_string)

        # Write the decoded data to a WAV file
        with open("query.wav", "wb") as wav_file:
            wav_file.write(wav_data)
        autoplay_audio('query.wav')
        
       
        
        st.session_state.messages.append({"role": "assistant", "content": result['output']})
