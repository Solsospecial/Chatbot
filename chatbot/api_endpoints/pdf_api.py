from fastapi import File, UploadFile, APIRouter
from starlette.responses import JSONResponse
from pydantic_models import QueryRequest
from pdf_data_collector import add_pdf_data, model, pdf_data_collection, client
import os
from pathlib import Path
from langchain_chroma import Chroma
import logging

logger = logging.getLogger(__name__)

# Initialize router
router = APIRouter()

UPLOAD_DIRECTORY = Path("upload")
os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)  # Ensure the directory exists

@router.post("/add_pdf/")
async def upload_pdf(file: UploadFile = File(...)):
    if not file.filename.endswith('.pdf'):
        return JSONResponse(status_code=400, content={"error": "Only PDF allowed"})
    file_path = UPLOAD_DIRECTORY / file.filename
    with open(file_path, "wb") as pdf_file:
        pdf_file.write(await file.read())
    logger.info(f"File saved successfully: {file_path}")
        
    try:
        add_pdf_data(pdf_file_path=file_path)
        return JSONResponse(status_code=200, content={"message": "PDF file uploaded and processed successfully."})
    except Exception as e:
        logger.exception("Error while processing PDF")
        return JSONResponse(status_code=500, content={"error": f"Failed to process the PDF file: {str(e)}"})
    
@router.post("/search_query_in_pdf/")
async def query_messages(request: QueryRequest):
    query=request.input
    collection1 = client.get_collection("pdf_data_collection")
    response_data = []
    print(collection1)
    db4 = Chroma(
        client=client,
        collection_name="pdf_data_collection",
        embedding_function=model,
    )
    
    print(collection1)
    print(query)
    result = db4.similarity_search(query=query)
    print(result)
    response_data = []
    extracted_data=""
    print(collection1)
    for results in result:
        metadata = results.metadata
        content=results.page_content
        extracted_data+=content
        extracted_data+=" "
    print(extracted_data)
    return extracted_data