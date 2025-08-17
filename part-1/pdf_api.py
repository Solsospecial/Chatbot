from fastapi import FastAPI, File, UploadFile, APIRouter
from starlette.responses import JSONResponse
from pathlib import Path
import os
import uuid
from langchain_community.document_loaders import PyPDFLoader
from sentence_transformers import SentenceTransformer
import chromadb

# Initialize FastAPI app and ChromaDB client
app = FastAPI()
router = APIRouter()
client = chromadb.Client()
UPLOAD_DIRECTORY = Path("upload")
os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)  # Ensure the upload directory exists

# Create a ChromaDB collection


# Load Sentence Transformer model for embeddings
model = SentenceTransformer('all-MiniLM-L6-v2')

@router.post("/process_pdf/")
async def process_pdf(file: UploadFile = File(...)):
    # Validate file type
    if not file.filename.endswith('.pdf'):
        return JSONResponse(status_code=400, content={"error": "Only PDF files are allowed."})

    # Save the uploaded file
    file_path = UPLOAD_DIRECTORY / file.filename
    with open(file_path, "wb") as pdf_file:
        pdf_file.write(await file.read())
        print("File saved successfully:", file_path)

    # Extract and clean text from the PDF
    try:
        loader = PyPDFLoader(file_path=str(file_path))
        documents = loader.load()
        print(documents)
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": f"Failed to process PDF file: {str(e)}"})

    # Generate a unique chat_id
    chat_id = "pdf_RAG"
    messages_collection = client.create_collection(chat_id)

    # Prepare documents, embeddings, and metadata for storing in ChromaDB
    doc_texts = [doc.page_content for doc in documents]
    embeddings = model.encode(doc_texts, convert_to_tensor=False)
    metadatas = [
        {
            'page_number': doc.metadata.get('page_number', idx + 1),
            'chat_id': chat_id  # Store chat_id in metadata
        } 
        for idx, doc in enumerate(documents)
    ]
    ids = [str(uuid.uuid4()) for _ in documents]

    # Store the documents and embeddings in the ChromaDB collection
    messages_collection.add(
        documents=doc_texts,
        embeddings=embeddings.tolist(),
        metadatas=metadatas,
        ids=ids,
    )

    # Return the chat_id and success message
    return JSONResponse(status_code=200, content={
        "chat_id": chat_id,
        "message": "PDF content processed and stored successfully."
    })
