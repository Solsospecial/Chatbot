from fastapi import APIRouter, BackgroundTasks
from fastapi.responses import JSONResponse
from web_data_collector import add_web_data, model, client
from langchain_chroma import Chroma
from pydantic_models import QueryRequest, WebDataRequest
import logging

logger = logging.getLogger(__name__)
router = APIRouter() # Initialize router

@router.post("/scrape_webdata/")
async def scrape_webdata(request: WebDataRequest, background_tasks: BackgroundTasks):
    # Scrape and store web data into ChromaDB
    try:
        url = request.url
        background_tasks.add_task(add_web_data, url)
        logger.info(f"Scraping task queued for URL: {url}")
        return JSONResponse(
            status_code=202,
            content={"message": f"Scraping started for {url}"}
        )
    except Exception as e:
        logger.error(f"Failed to scrape {request.url}: {e}")
        return JSONResponse(
            status_code=500,
            content={"error": f"Failed to scrape web data: {str(e)}"}
        )
        
@router.post("/search_query_in_web/")
async def query_messages(request: QueryRequest):
    # Extract query from request
    query = request.input
    
    try:
        # Initialize Chroma object for the collection
        db = Chroma(
            client=client,
            collection_name="web_data_collection",
            embedding_function=model,
        )
        
        # Perform a similarity search using the query
        results = db.similarity_search(query=query, k=5)
        
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
    
    
    
    
    