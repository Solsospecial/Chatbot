import chromadb
import uuid
from langchain.document_loaders import PyPDFLoader
from langchain_huggingface import HuggingFaceEmbeddings

client = chromadb.Client()
messages_collection = client.get_or_create_collection("messages_collection")
model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

def load_pdf(pdf_file_path):
    try:
        loader = PyPDFLoader(pdf_file_path)
        data = loader.load()
        print(len(data))
        return data
    except Exception as e:
        print(f"Error loading PDF file: {str(e)}")
        return None

def process_messages(data):
    if data is None:
        print("Nothing is present")
        return False

    # Prepare documents, embeddings, metadata, and ids
    documents, metadata, ids = [], [], []

    for index, document in enumerate(data):
        # Extract document content from embedding
        documents.append(document.page_content)

        # Prepare metadata
        metadata.append({
            'page_number': document.metadata.get('page_number', index + 1)
        })

        ids.append(str(uuid.uuid4()))  # Generate unique IDs for each chunk
    print(metadata)

    # Embed the documents
    embeddings = model.embed_documents(documents)

    # Add documents to the ChromaDB collection
    messages_collection.add(
        documents=documents,
        embeddings=embeddings,
        metadata=metadata,
        ids=ids
    )

    num_of_docs = len(documents)
    print(f"Stored {num_of_docs} document{'' if num_of_docs < 2 else 's'} in ChromaDB.")
    return True
    
def add_linkedin_messages(pdf_file_path):
    # Load messages from PDF
    print("Loading Messages...")
    messages_df = load_pdf(pdf_file_path)
    
    # Process messages and add to ChromaDB collection
    if process_messages(messages_df):
        print("PDF processing complete.")