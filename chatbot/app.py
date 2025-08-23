import streamlit as st
import os
import requests
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_tool_calling_agent, AgentExecutor
from tools import pdf_tool, web_tool, google_tool
from prompt import prompt

# Streamlit configuration
st.set_page_config(page_title="Streamlit Chatbot for PDF Query and Web Search")

# Setup API Key with validation
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    st.error("GEMINI_API_KEY is not set. Please set it in environment variables.")
    st.stop()
    
# Initialize tools/prompt in session state
if "pdf_tool" not in st.session_state:
    st.session_state.pdf_tool = pdf_tool()

if "web_tool" not in st.session_state:
    st.session_state.web_tool = web_tool()

if "google_tool" not in st.session_state:
    st.session_state.google_tool = google_tool()

if "prompt" not in st.session_state:
    st.session_state.prompt = prompt()

if "messages" not in st.session_state:
    st.session_state.messages = []
    
# For the chatbot's greeting message
if "initialized_greeting" not in st.session_state:
    st.session_state.initialized_greeting = False

# Streamlit setup
st.title("Streamlit Chatbot with PDF and Web Search")
        
with st.sidebar:
    file_uploader = st.file_uploader("Upload your file:", type=["pdf"])
    url = st.text_input("Enter URL").strip()
    if file_uploader is not None and "upload_pdf" not in st.session_state:
        response = requests.post(f"http://127.0.0.1:8000/add_pdf/", files={"file": file_uploader})
        if response.status_code == 200:
            st.success("Messages added successfully")
        st.session_state.upload_pdf = True

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
        st.session_state.url = True
        
# Create the LangChain agent
if "agent_executor" not in st.session_state:
    try:
        llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", max_retries=2)
        
        # Setup tools
        tools = [
            st.session_state.google_tool,
            st.session_state.pdf_tool,
            st.session_state.web_tool
        ]
        
        agent = create_tool_calling_agent(llm, tools, st.session_state.prompt)
        st.session_state.agent_executor = AgentExecutor(
            agent=agent,
            tools=tools,
            verbose=True,
            handle_parsing_errors=True,
            max_iterations=10
        )
    except Exception as e:
        st.error(f"Failed to initialize agent: {e}")
        st.stop()
    
# Show existing messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        
# Initialize geeting once
if not st.session_state.initialized_greeting:
    greeting = "Hi there! How can I help you? 😊"
    with st.chat_message("assistant"):
        st.markdown(greeting)
    st.session_state.messages.append({"role": "assistant", "content": greeting})
    st.session_state.initialized_greeting = True

# Handle text input
if query := st.chat_input("Enter your query:"):
    st.session_state.messages.append({"role": "user", "content": query})
    with st.chat_message("user"):
        st.markdown(query)
    with st.spinner("Generating response..."):
        try:
            result = st.session_state.agent_executor.invoke({
                "input": query,
                "chat_history": st.session_state.messages[-30:]
            })
            output = result["output"]
        except Exception as e:
            output = f"Sorry, I ran into an error: {e}"
        
    with st.chat_message("assistant"):
        st.markdown(output)
    st.session_state.messages.append({"role": "assistant", "content": output})