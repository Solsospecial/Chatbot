
from fastapi import FastAPI, HTTPException, Depends, File, UploadFile, BackgroundTasks, APIRouter
from starlette.responses import HTMLResponse, JSONResponse
from pydantic_models import QueryRequest
from typing import List
from chrome import add_linkedin_messages, model, messages_collection,client  # Assuming these are imported correctly
import os
from pathlib import Path
import chromadb
import uuid
from langchain_chroma import Chroma
import logging
# from langchain_community.document_loaders.csv_loader import CSVLoader
import json
from langchain_community.document_loaders import PyPDFLoader
# from gmail_loader import get_access_token, get_emails
# from db_utils import add_token, get_token
# persistent_client = chromadb.PersistentClient()
# collection = persistent_client.create_collection("messages_collectionn")

logger = logging.getLogger(__name__)
# router = APIRouter()
router = APIRouter()

UPLOAD_DIRECTORY = Path("upload")
os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)  # Ensure the directory exists
# @router.get("/post/")
# async def main():
#     return "Hi"

@router.post("/add_pdf/")
async def upload_csv(file: UploadFile = File(...)):
    # print(bot_id)
    if not file.filename.endswith('.pdf'):
        return JSONResponse(status_code=400, content={"error": "Only PDF allowed"})
    file_path = UPLOAD_DIRECTORY / file.filename
    with open(file_path, "wb") as pdf_file:
        pdf_file.write(await file.read())
        print("File saved successfully:", file_path)
        
    try:
        add_linkedin_messages(pdf_file_path=file_path)
        return JSONResponse(status_code=200, content={"message": "LinkedIn messages uploaded and processed successfully."})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": f"Failed to process CSV file: {str(e)}"})
    

@router.post("/search_query_in_pdf/")
async def query_messages(request: QueryRequest):
    query=request.input
    collection1 = client.get_collection("messages_collection")
    response_data = []
    print(collection1)
    db4 = Chroma(
    client=client,
    collection_name="messages_collection",
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
        # metadata_sender = metadata.get('FROM', 'Unknown')
        # recipient = metadata.get('TO', 'Unknown')
        # content = metadata.get('CONTENT', 'No content available')
        # metadata_bot_id = metadata.get('bot_id', 'No bot_id available')
        print("bot_id")
        # print(bot_id)
        # print(type(bot_id))
        # print(type(metadata_bot_id))
        # print(metadata_bot_id)
        # if 
        # if str(metadata_bot_id)==str(bot_id):
            # print("pass")
            # if receiver == "string" or receiver==None or receiver=="":
                # print("pass-1")
        extracted_data+=content
        extracted_data+=" "
    print(extracted_data)
    return extracted_data

