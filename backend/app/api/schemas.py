from pydantic import BaseModel
from typing import Optional, Any, List, Dict

class ChatRequest(BaseModel):
    user_id: str
    text: Optional[str] = None
    link: Optional[str] = None
    model: Optional[str] = None

class ChatResponse(BaseModel):
    answer: str
    meta: Optional[Dict[str, Any]] = {}

class UploadResponse(BaseModel):
    answer: str
    meta: Optional[Dict[str, Any]] = {}

class TranscribeResponse(BaseModel):
    transcript: str
    meta: Optional[Dict[str, Any]] = {}
