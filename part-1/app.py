import streamlit as st
from dotenv import load_dotenv
import os
import requests

from langchain_core.prompts import ChatPromptTemplate
# from langchain_groq import ChatGroq
from pydantic_models import QueryRequest
from langchain_openai import ChatOpenAI
from langchain.agents import create_openai_tools_agent
from langchain.agents import AgentExecutor



load_dotenv()



# Setup API Keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Google Search Tool

# uploaded_file = st.sidebar.file_uploader("Upload a PDF file", type=["pdf"])
# url = st.sidebar.text_input("Enter URL")

with st.sidebar:
    file_uploader=st.file_uploader("Upload your file:", type=["pdf"])
    if file_uploader is not None and "pdf" not in st.session_state:
    # Send the uploaded file to the new API endpoint
        response = requests.post(
            "http://127.0.0.1:8000/process_pdf/",
            files={"file": file_uploader},
        )
        
        # Handle the API response
        if response.status_code == 200:
            # Extract chat_id from the response if needed
            chat_id = response.json().get("chat_id")
            st.success(f"PDF processed successfully with Chat ID: {chat_id}")
            st.session_state.pdf = chat_id
        else:
            # Display error message from the response
            error_message = response.json().get("error", "An error occurred while processing the PDF.")
            st.error(error_message)


if "messages" not in st.session_state:
   st.session_state.messages = []


if (file_uploader is None):
    st.info("please upload your pdf")

else:
    code=st.session_state['pdf']
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown (message["content"])

    if "prompt" not in st.session_state:
        chat = ChatOpenAI(model="gpt-3.5-turbo-0125", temperature=0, api_key=OPENAI_API_KEY)
        system = "You are a helpful assistant, you are provided the content{content} from my vector database based on query, you need to structure the response as per the query{input}. ALso Chat history is provided to you, you can use {history} if any followed up question is given."
        human = "{input},{content},{history}"
        prompt = ChatPromptTemplate.from_messages(
            [("system", system), 
            ("human", human)]
            )
        st.session_state.chain = prompt | chat
        st.session_state.prompt="Existing"
    
    if query:=st.chat_input("Enter your query"):
        st.session_state.messages.append({"role": "user", "content": query})
        with st.chat_message("user"):
            st.markdown(query)
        try:
            response = requests.post(
                "http://127.0.0.1:8000/search_query/",
                json={"chat_id": code, "query": query}
            )

            # Handling the response from the server
            if response.status_code == 200:
                extracted_data = response.json()  # Expecting a string response
                st.success("Query executed successfully!")
                # st.write("**Extracted Content:**")
                with st.expander("**Extracted Content:**"):
                    st.write(extracted_data)
            else:
                error_message = response.json().get("detail", "An error occurred during the search.")
                st.error(f"Error: {error_message}")

        except requests.exceptions.RequestException as e:
            st.error(f"An error occurred while connecting to the server: {str(e)}")

        with st.spinner("Generating response..."):
            with st.chat_message("assistant"):
                messages = st.session_state.messages
                messages_str = ""
                for message in messages:
                    if message["role"] == "user":
                        messages_str += f"User: {message['content']}///"
                    elif message["role"] == "assistant":
                        messages_str += f"Assistant: {message['content']}///"
                print(messages_str)
                result = st.session_state.chain.invoke({"input": query,"content":extracted_data,"history":messages_str})
                st.markdown(result.content)
                st.session_state.messages.append({"role": "assistant", "content": result.content})
                # st.write(result['output'])


