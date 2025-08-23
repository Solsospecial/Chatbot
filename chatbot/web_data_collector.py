import chromadb
import uuid
from langchain_community.document_loaders import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings

client = chromadb.Client()
web_data_collection = client.get_or_create_collection("web_data_collection")

# Initialize the Sentence Transformer model
model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

def load_web_data(url):
    try:
        # Create a WebBaseLoader instance with the provided URL
        loader = WebBaseLoader(url)
        
        # Load the web page conten
        data = loader.load()
        
        # Split into chunks
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=800,
            chunk_overlap=100
        )
        document_chunks = text_splitter.split_documents(data)
        
        print(f"Loaded {len(document_chunks)} documents from {url}")
        return document_chunks

    except Exception as e:
        print(f"Error loading web data: {str(e)}")
        return None

def process_web_data(data):
    if data is None:
        print("No data to process.")
        return False
    
    # Prepare documents, embeddings, metadata, and ids
    documents, metadatas, ids = [], [], []

    for index, document in enumerate(data):
        # Extract document content for embedding
        documents.append(document.page_content)

        # Prepare metadatas
        metadatas.append({
            'source_url': document.metadata.get('source', 'unknown'),
            'chunk_number': index + 1
        })
        
        ids.append(str(uuid.uuid4()))  # Generate unique IDs for each document

    # Embed the documents
    embeddings = model.embed_documents(documents)
    
    # Add documents to the ChromaDB collection
    web_data_collection.add(
        documents=documents,
        embeddings=embeddings,
        metadatas=metadatas,
        ids=ids
    )
    
    num_of_docs = len(documents)
    print(f"Stored {num_of_docs} document{'' if num_of_docs < 2 else 's'} in ChromaDB.")
    return True

def add_web_data(url):
    # Load web data from the given URL
    print(f"Loading data from {url}...")
    web_data = load_web_data(url)

    # Process web data and add it to the ChromaDB collection
    if process_web_data(web_data):
        print("Web data processing complete.")