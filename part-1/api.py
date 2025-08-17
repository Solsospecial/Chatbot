import pdf_api,search_api
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from prometheus_fastapi_instrumentator import Instrumentator
from starlette.middleware.sessions import SessionMiddleware
import logging


logging.basicConfig(filename='api.log', filemode='a', level=logging.INFO, \
                    format='%(asctime)s - %(name)s - %(levelname)s - %(funcName)s - %(lineno)d- %(message)s')
app = FastAPI()

Instrumentator().instrument(app).expose(app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add the SessionMiddleware to enable session handling
app.add_middleware(SessionMiddleware, secret_key="your-secret-key")

app.include_router(pdf_api.router, tags=["PDF Question Answering"])
# app.include_router(web_api.router, tags=["Website Question Answering"])
app.include_router(search_api.router, tags=["Search for query"])
# app.include_router(bot_details.router, tags=["Bot Details"])
# app.include_router(response.router, tags=["Get Answer"])
# app.include_router(linkedin_api.router, tags=["Linkedin messages Operations"])

