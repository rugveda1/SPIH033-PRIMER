from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class ChatMessageIn(BaseModel):
    message: str
    concept_id: int

class ChatMessageOut(BaseModel):
    id: int
    role: str
    content: str
    timestamp: datetime

    model_config = {
        "from_attributes": True
    }

class ChatSessionOut(BaseModel):
    id: int
    concept_id: Optional[int]
    created_at: datetime
    messages: List[ChatMessageOut] = []

    model_config = {
        "from_attributes": True
    }

class ChatHintIn(BaseModel):
    concept_id: int
    question_id: Optional[int] = None

class ChatExplainIn(BaseModel):
    concept_id: int
