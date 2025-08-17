from pydantic import BaseModel
from typing import Optional
class QueryRequest(BaseModel):
    chat_id: str
    query: str
    # chat_id: str  # New field for specifying the bot_id

class MessageResponse(BaseModel):
    # id: str
    content: str

class WebDataRequest(BaseModel):
    url: str