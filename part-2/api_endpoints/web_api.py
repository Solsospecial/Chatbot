from fastapi import FastAPI, Form
from fastapi import FastAPI, HTTPException, Depends, File, UploadFile, BackgroundTasks, APIRouter

from fastapi.responses import JSONResponse
from langchain_community.document_loaders import WebBaseLoader
from chroma_web import add_web_data, model, messages_collection,client 
import chromadb
from langchain_chroma import Chroma

from pydantic_models import QueryRequest,WebDataRequest
router = APIRouter()

@router.post("/scrape_webdata/")
async def scrape_webdata(request: WebDataRequest):
    try:
        url = request.url
        # Create a WebBaseLoader instance with the provided URL
        add_web_data(url)
        
        return JSONResponse(status_code=200, content={"message": "Web data scraped successfully."})
    
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": f"Failed to scrape web data: {str(e)}"})

@router.post("/search_query_in_web/")
async def query_messages(request: QueryRequest):
    # Extract query from request
    query = request.input
    
    # Access the ChromaDB collection
    collection1 = client.get_collection("webdata_collection")
    
    # Initialize Chroma object for the collection
    db = Chroma(
        client=client,
        collection_name="webdata_collection",
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