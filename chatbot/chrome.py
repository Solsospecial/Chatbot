import chromadb
from sentence_transformers import SentenceTransformer
import pandas as pd
import uuid
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_community.document_loaders import PyPDFLoader

client = chromadb.Client()
messages_collection = client.create_collection("messages_collection")
model = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

def load_pdf(pdf_file_path):
    try:
        loader = PyPDFLoader(file_path=pdf_file_path)
        data = loader.load()
        print(len(data))
        return data
    except Exception as e:
        print(f"Error loading PDF file: {str(e)}")
        return None

def process_messages(data):
    if data is None:
        print("Nothing is present")
        return
    model = SentenceTransformer('all-MiniLM-L6-v2')

    # Prepare documents, embeddings, metadata, and ids
    documents = []
    metadata = []
    ids = []

    for index, document in enumerate(data):
        # Extract page content from the document
        content = document.page_content

        # Prepare metadata
        meta_data = {
            'page_number': document.metadata.get('page_number', index + 1),
        }
        metadata.append(meta_data)

        # Collect document content for embedding
        documents.append(content)
        ids.append(str(uuid.uuid4()))  # Generate unique IDs for each chunk
    print(metadata)
    print(documents)

    # Embed the documents
    embeddings = model.encode(documents, convert_to_tensor=True)

    # Add documents to the ChromaDB collection
    messages_collection.add(
        documents=documents,
        embeddings=embeddings.tolist(),  # Convert embeddings to a list
        metadata=metadata,
        ids=ids,
    )

    num_of_docs = len(documents)
    print(f"Stored {num_of_docs} document{'' if num_of_docs < 2 else 's'} in ChromaDB.")

def add_linkedin_messages(pdf_file_path):
    # Load messages from PDF
    print("Loadng Messages.")
    messages_df = load_pdf(pdf_file_path)
    
    # Process messages and add to ChromaDB collection
    process_messages(messages_df)
    print("Processing")