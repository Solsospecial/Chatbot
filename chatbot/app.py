import streamlit as st
import os
import requests
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain.memory import ConversationBufferWindowMemory
from tools import pdf_tool, web_tool, google_tool
from prompt import prompt

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

# Initialize LangChain memory
if "memory" not in st.session_state:
    st.session_state.memory = ConversationBufferWindowMemory(
        memory_key="chat_history",
        k=10,   # Keep last 10 conversation turns only
        return_messages=True
    )

# Set flag for the chatbot's greeting message
if "initialized_greeting" not in st.session_state:
    st.session_state.initialized_greeting = False

# Streamlit configuration
st.set_page_config(page_title="Streamlit Chatbot for PDF Query and Web Search")

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
        
        agent = create_tool_calling_agent(
            llm,
            tools,
            st.session_state.prompt,
            memory=st.session_state.memory
        )
        
        st.session_state.agent_executor = AgentExecutor(
            agent=agent,
            tools=tools,
            verbose=True,
            handle_parsing_errors=True,
            max_iterations=5
        )
    except Exception as e:
        st.error(f"Failed to initialize agent: {e}")
        st.stop()
    
# Show existing messages from memory
for msg in st.session_state.memory.chat_memory.messages:
    role = msg.type  # 'human' or 'ai'
    content = msg.content
    with st.chat_message(role):
        st.markdown(content)
        
# Initialize geeting once
if not st.session_state.initialized_greeting:
    greeting = "Hi there! How can I help you?"
    with st.chat_message("assistant"):
        st.markdown(greeting)
    st.session_state.memory.chat_memory.add_ai_message(greeting)
    st.session_state.initialized_greeting = True

# Handle text input
if query := st.chat_input("Enter your query:"):
    st.session_state.memory.chat_memory.add_user_message(query)
    with st.chat_message("user"):
        st.markdown(query)
    with st.spinner("Generating response..."):
        try:
            result = st.session_state.agent_executor.invoke({"input": query})
            output = result["output"]
        except Exception as e:
            output = f"Sorry, I ran into an error: {e}"
        
    with st.chat_message("assistant"):
        st.markdown(output)
    st.session_state.memory.chat_memory.add_ai_message(output)