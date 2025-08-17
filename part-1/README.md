# Chatbot with pdf and web url using API

## Overview
This project is a chatbot that allows users to ask questions specifically about a PDF file. The chatbot uses a combination of Large Language Models (LLMs) and a vector database to store and retrieve relevant information from the PDF.

We have developed a custom API using the FastAPI framework. The content of the PDF is divided into chunks and stored in ChromaDB, with a fixed chat_id used to manage and retrieve these chunks. The chat_id is used to fetch the relevant information from the collection based on the user’s query.

Once the appropriate chunk is retrieved, we use an OpenAI model to generate a response, providing the user with accurate answers derived from the content of the PDF.

## Prerequisites

- Python 3.8 or above

## Installation
```bash
pip install -r requirements.txt
```
## Setup Instructions

### Step 1: Clone or download the Repository (if emailed)

```bash
git https://github.com/venkatavinayvijjapu/sarvam.git
cd part-1
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

Create a `.env` file in the root directory and add your OpenAI API keys in a way it can be accessed in the app.

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
- **pdf_api**: Contains the endpoint to process the pdf and generate the chat_id and to store the documents contents into chromadb.
- **search_api**: Contains the endpoint to search the query in the vector database based on the chat_id generated and retrive the relevant chunks from the database and pass it to the LLM model to generate the response.
- **app.py**: Contains the streamlit code for the front end and interaction with the user.
- **.env**: Stores API keys (make sure this file is not included in version control).
- **requirements.txt**: Lists the project dependencies.

## Video Prototype:
You can watch the demo video [here](https://www.veed.io/view/501eac97-73b7-4996-a275-d9f8ef061d30?panel=share).
