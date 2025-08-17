# Chatbot with pdf and web url using API

## Overview
This project is an intelligent agent that allows users to ask questions about a particular PDF file, a web URL, or perform a Google search. The agent combines Large Language Models (LLMs) and a vector database for efficient storage and retrieval of relevant information for pdf data and URL data.

We have created a custom API using the FastAPI framework, where collections are stored in ChromaDB. Two collections are made in chromadb where we use to get chunks from the collection based on the type of agent invoked. The retrieval process is based on the context provided by the user.

The agent supports three primary search methods:

- Google Search: Users can ask questions that are answered through real-time Google searches.
- PDF Search: The agent can parse and search through PDF documents provided by the user to find relevant content.
- Provided URL Search: Users can input a web URL, and the agent will extract relevant information from the webpage to answer queries.
Once the relevant chunk of information is retrieved (from the vector database, PDF, or the web), we use an OpenAI model to generate a contextual response for the user.



## Prerequisites

- Python 3.8 or above

## Installation
```bash
pip install -r requirements.txt
```
## Setup Instructions

### Step 1: Clone or download the Repository (if emailed)

```bash
git clone https://github.com/venkatavinayvijjapu/sarvam.git
cd part-2
```
### Step 2: Set Up a Virtual Environment

You can use `venv` or `conda` to create an isolated environment for this project.
#### Using `venv`

```bash
python -m venv env
source env/bin/activate  # On Windows, use `env\Scripts\activate`
```

#### Using `conda`

```bash
conda create --name project_env python=3.8
conda activate project_env
```

## Step 4: Set Up Environment Variables

Create a `.env` file in the root directory and add your OpenAI API keys, GOOGLE_API KEY and GOOGLE org id in a way it can be accessed in the app.

### step 5: Run the API 
```bash
python -m uvicorn api:app --reload
```

### step 6: Run the Streamlit app

```bash
python -m streamlit run app.py
```

### Step 7: Open the Application

Open your web browser and go to `http://localhost:8501`. You can now add you pdf and url and interact with the system by entering your query and selecting the type pdf pr url in select box.

## Project Structure

- **api**: Routes for all the api endpoints i.e pdf_api,web_api,search_api
- **api_endpoints**: Contains PDF_API and WEB_API which is used to store data and retrive data from chromadb. pdf_api and web_api has two endpoints in each to store and retrive data.
- **app.py**: Contains the streamlit code for the front end and interaction with the user.
- **.env**: Stores API keys (make sure this file is not included in version control).
- **pydantic_models**: Contains some base version of the data need to passed to endpoints and the format of the data need to be fetched from endpoints.
- **prompt**: Generates prompt required for the LLM's.
- **pdf_wrapper**: This wrapper is to call the api-endpoints based on the query this wrapper function executes and calls the endpoints. This wrapper class is specially for pdf endpoints.
- **web_wrapper**: This wrapper is to call the api-endpoints based on the query this wrapper function executes and calls the endpoints. This wrapper class is specially for web endpoints.
- **gpt_utils**: Creates all the types of tools.
- **requirements.txt**: Lists the project dependencies.

## Video Prototype:
You can watch the demo video [here](https://www.veed.io/view/04cda54d-7903-4339-ab40-9a43dd85cf16?panel=share).
