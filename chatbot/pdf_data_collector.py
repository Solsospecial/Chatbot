import chromadb
import uuid
from langchain_community.document_loaders import PyPDFLoader
from langchain_huggingface import HuggingFaceEmbeddings

client = chromadb.Client()
pdf_data_collection = client.get_or_create_collection("pdf_data_collection")
model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

def load_pdf(pdf_file_path):
    try:
        loader = PyPDFLoader(pdf_file_path, mode="page")
        data = loader.load()
        return data
    except Exception as e:
        print(f"Error loading PDF file: {str(e)}")
        return None

def process_pdf_data(data):
    if data is None:
        print("Nothing is present")
        return False

    # Prepare documents, embeddings, metadata, and ids
    documents, metadata, ids = [], [], []
    print("nonsense place")
    for index, document in enumerate(data):
        # Extract document content from embedding
        documents.append(document.page_content)

        # Prepare metadata
        metadata.append({'page_number': index + 1})

        ids.append(str(uuid.uuid4()))  # Generate unique IDs for each chunk
    print("Done pdf metafata prep")
    # Embed the documents
    embeddings = model.embed_documents(documents)
    print("Finished embeddings")
    # Add documents to the ChromaDB collection
    pdf_data_collection.add(
        documents=documents,
        embeddings=embeddings,
        metadatas=metadata,
        ids=ids
    )
    print("collection creatwz")
    num_of_docs = len(documents)
    print(f"Stored {num_of_docs} document{'' if num_of_docs < 2 else 's'} in ChromaDB.")
    return True
    
def add_pdf_data(pdf_file_path):
    # Load data from PDF
    print("Loading PDF data...")
    pdf_data_df = load_pdf(pdf_file_path)
    
    # Process PDF data and add to ChromaDB collection
    if process_pdf_data(pdf_data_df):
        print("PDF processing complete.")