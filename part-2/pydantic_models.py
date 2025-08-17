from pydantic import BaseModel
from typing import Optional
class QueryRequest(BaseModel):
    input: str
    # bot_id: str  # New field for specifying the bot_id

class MessageResponse(BaseModel):
    # id: str
    content: str

class WebDataRequest(BaseModel):
    url: str