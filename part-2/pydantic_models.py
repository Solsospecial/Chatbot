from langchain_core.pydantic_v1 import BaseModel

class QueryRequest(BaseModel):
    input: str

class MessageResponse(BaseModel):
    content: str

class WebDataRequest(BaseModel):
    url: str