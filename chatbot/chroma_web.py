import chromadb
import pandas as pd
import uuid
from langchain_community.document_loaders import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings

client = chromadb.Client()
web_data_collection = client.get_or_create_collection("webdata_collection")

# Initialize the Sentence Transformer model
model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")

def load_web_data(url):
    try:
        # Create a WebBaseLoader instance with the provided URL
        loader = WebBaseLoader(url)
        
        # Load the web page content
        data = loader.load()
        document_chunks = RecursiveCharacterTextSplitter().split_documents(data)
        print(f"Loaded {len(document_chunks)} documents from {url}")
        print(document_chunks)
        return document_chunks

    except Exception as e:
        print(f"Error loading web data: {str(e)}")
        return None

def process_web_data(data):
    if data is None:
        print("No data to process.")
        return False
    
    # Prepare documents, embeddings, metadata, and ids
    documents = []
    metadata = []
    ids = []

    for index, document in enumerate(data):
        # Extract page content from the document
        content = document.page_content

        # Prepare metadata
        meta_data = {
            'source_url': document.metadata.get('source', 'unknown'),
            'page_number': document.metadata.get('page_number', index + 1),
        }
        metadata.append(meta_data)

        # Collect document content for embedding
        documents.append(content)
        ids.append(str(uuid.uuid4()))  # Generate unique IDs for each document
    print(metadata)
    print(documents)

    # Embed the documents
    embeddings = model.encode(documents, convert_to_tensor=True)
    
    # Add documents to the ChromaDB collection
    web_data_collection.add(
        documents=documents,
        embeddings=embeddings.tolist(),  # Convert embeddings to a list
        metadata=metadata,
        ids=ids,
    )
    
    num_of_docs = len(documents)
    print(f"Stored {num_of_docs} document{'' if num_of_docs < 2 else 's'} in ChromaDB.")
    return True

def add_web_data(url):
    # Load web data from the given URL
    print(f"Loading data from {url}")
    web_data = load_web_data(url)

    # Process web data and add it to the ChromaDB collection
    if process_web_data(web_data):
        print("Web data processing complete.")