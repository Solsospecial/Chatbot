from fastapi import FastAPI, Form
from fastapi import FastAPI, HTTPException, Depends, File, UploadFile, BackgroundTasks, APIRouter
from sentence_transformers import SentenceTransformer
from fastapi.responses import JSONResponse
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.embeddings import SentenceTransformerEmbeddings
# from chroma_web import add_web_data, model, messages_collection,client 
import chromadb
from langchain_chroma import Chroma
from pydantic_models import QueryRequest,WebDataRequest
router = APIRouter()
@router.post("/search_query/")
async def query_messages(request: QueryRequest):
    # Extract query from request
    query = request.query
    collection_name=request.chat_id
    client = chromadb.Client()
    model = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

    # Access the ChromaDB collection
    collection1 = client.get_collection(collection_name)
    
    # Initialize Chroma object for the collection
    db = Chroma(
        client=client,
        collection_name=collection_name,
        embedding_function=model,
    )
    
    # Perform a similarity search using the query
    result = db.similarity_search(query=query)
    
    # Extract relevant content and metadata from the results
    response_data = []
    extracted_data=''
    for results in result:
        metadata = results.metadata
        content = results.page_content
        
        # Construct the search result
        extracted_data+=content
        extracted_data+=' '
    print(extracted_data)
    
    # Return the search results
    return extracted_data