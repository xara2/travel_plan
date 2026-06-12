from pydantic import BaseModel
from datetime import datetime


class ChatRequest(BaseModel):
    conversation_id: int | None = None
    message: str
    context: dict = {}


class ChatResponse(BaseModel):
    conversation_id: int
    message: str
    tool_calls: list[dict] = []
    attractions_found: list[str] = []


class ConversationOut(BaseModel):
    id: int
    title: str
    created_at: str
    updated_at: str
    message_count: int = 0

    model_config = {"from_attributes": True}


class MessageOut(BaseModel):
    id: int
    role: str
    content: str
    metadata: dict = {}
    created_at: str

    model_config = {"from_attributes": True}


class ConversationDetail(BaseModel):
    id: int
    title: str
    messages: list[MessageOut] = []
    created_at: str
    updated_at: str

    model_config = {"from_attributes": True}


class ConversationUpdate(BaseModel):
    title: str
