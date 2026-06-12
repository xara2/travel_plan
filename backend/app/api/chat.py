"""Chat and conversation API endpoints."""
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from ..database import get_db
from ..utils.auth import get_current_user
from ..models.user import User
from ..models.conversation import Conversation, Message
from ..schemas.chat import (
    ChatRequest, ChatResponse, ConversationOut,
    MessageOut, ConversationDetail, ConversationUpdate,
)
from ..agent.react_agent import ReActAgent, ConversationMemory
from ..agent.tool_registry import get_tool_registry
from ..agent.tools import search_attractions_tool, generate_plan_tool, search_images_tool

router = APIRouter(prefix="/api", tags=["chat"])

# Register tools at module load
_registry = get_tool_registry()
_registry.register(
    "search_attractions",
    "语义搜索景点。参数: query(搜索关键词), city(城市可选), category(类别可选), top_k(数量)",
    search_attractions_tool,
    {"query": "string", "city": "string", "category": "string", "top_k": "integer"},
)
_registry.register(
    "generate_plan",
    "根据景点ID列表生成旅行计划。参数: attraction_ids(JSON数组), destination(目的地), duration(天数), preferences(偏好可选)",
    generate_plan_tool,
    {"attraction_ids": "string", "destination": "string", "duration": "integer", "preferences": "string"},
)
_registry.register(
    "search_images",
    "搜索景点图片。参数: query(关键词), destination(目的地), count(数量)",
    search_images_tool,
    {"query": "string", "destination": "string", "count": "integer"},
)


@router.post("/chat", response_model=ChatResponse)
async def send_message(
    req: ChatRequest,
    user: User = Depends(get_current_user),
    pg_db: Session = Depends(get_db),
):
    agent = ReActAgent()

    # Get or create conversation
    if req.conversation_id:
        conversation = pg_db.query(Conversation).filter(
            Conversation.id == req.conversation_id,
            Conversation.user_id == user.id,
        ).first()
        if not conversation:
            raise HTTPException(status_code=404, detail="对话不存在")
    else:
        title = req.message[:30] + ("..." if len(req.message) > 30 else "")
        conversation = Conversation(user_id=user.id, title=title)
        pg_db.add(conversation)
        pg_db.flush()

    # Save user message
    user_msg = Message(
        conversation_id=conversation.id,
        role="user",
        content=req.message,
    )
    pg_db.add(user_msg)
    pg_db.flush()

    # Reload conversation with messages for memory
    conversation = pg_db.query(Conversation).filter(
        Conversation.id == conversation.id,
    ).first()
    memory = ConversationMemory(conversation)

    # Run agent
    response_text = await agent.run(memory, req.message)

    # Save assistant message
    assistant_msg = Message(
        conversation_id=conversation.id,
        role="assistant",
        content=response_text,
    )
    pg_db.add(assistant_msg)

    conversation.title = _derive_title(conversation.title, req.message)
    pg_db.commit()

    return ChatResponse(
        conversation_id=conversation.id,
        message=response_text,
        attractions_found=_extract_attraction_mentions(response_text),
    )


@router.post("/chat/stream")
async def send_message_stream(
    req: ChatRequest,
    user: User = Depends(get_current_user),
    pg_db: Session = Depends(get_db),
):
    """SSE streaming chat endpoint."""
    agent = ReActAgent()

    # Get or create conversation
    if req.conversation_id:
        conversation = pg_db.query(Conversation).filter(
            Conversation.id == req.conversation_id,
            Conversation.user_id == user.id,
        ).first()
        if not conversation:
            raise HTTPException(status_code=404, detail="对话不存在")
    else:
        title = req.message[:30] + ("..." if len(req.message) > 30 else "")
        conversation = Conversation(user_id=user.id, title=title)
        pg_db.add(conversation)
        pg_db.flush()

    # Save user message
    user_msg = Message(
        conversation_id=conversation.id,
        role="user",
        content=req.message,
    )
    pg_db.add(user_msg)
    pg_db.flush()

    conversation = pg_db.query(Conversation).filter(
        Conversation.id == conversation.id,
    ).first()
    memory = ConversationMemory(conversation)
    messages = memory.build_messages()
    messages.append({"role": "user", "content": req.message})

    async def event_stream():
        full_response = ""
        try:
            async for chunk in agent.llm.chat_stream(
                messages=messages, temperature=0.7, max_tokens=2000,
            ):
                full_response += chunk
                yield f"data: {chunk}\n\n"
            yield "data: [DONE]\n\n"
        except Exception as e:
            yield f"data: [ERROR] {str(e)}\n\n"
        finally:
            assistant_msg = Message(
                conversation_id=conversation.id,
                role="assistant",
                content=full_response,
            )
            pg_db.add(assistant_msg)
            pg_db.commit()

    return StreamingResponse(event_stream(), media_type="text/event-stream")


@router.get("/conversations", response_model=list[ConversationOut])
def list_conversations(
    user: User = Depends(get_current_user),
    pg_db: Session = Depends(get_db),
):
    conversations = (
        pg_db.query(Conversation)
        .filter(Conversation.user_id == user.id)
        .order_by(Conversation.updated_at.desc())
        .all()
    )
    return [
        ConversationOut(
            id=c.id,
            title=c.title,
            created_at=c.created_at.isoformat() if c.created_at else "",
            updated_at=c.updated_at.isoformat() if c.updated_at else "",
            message_count=len(c.messages) if c.messages else 0,
        )
        for c in conversations
    ]


@router.get("/conversations/{conv_id}", response_model=ConversationDetail)
def get_conversation(
    conv_id: int,
    user: User = Depends(get_current_user),
    pg_db: Session = Depends(get_db),
):
    conversation = pg_db.query(Conversation).filter(
        Conversation.id == conv_id,
        Conversation.user_id == user.id,
    ).first()
    if not conversation:
        raise HTTPException(status_code=404, detail="对话不存在")

    messages = sorted(conversation.messages, key=lambda m: m.created_at or "")
    return ConversationDetail(
        id=conversation.id,
        title=conversation.title,
        created_at=conversation.created_at.isoformat() if conversation.created_at else "",
        updated_at=conversation.updated_at.isoformat() if conversation.updated_at else "",
        messages=[
            MessageOut(
                id=m.id,
                role=m.role,
                content=m.content,
                metadata=m.metadata_json or {},
                created_at=m.created_at.isoformat() if m.created_at else "",
            )
            for m in messages
        ],
    )


@router.delete("/conversations/{conv_id}")
def delete_conversation(
    conv_id: int,
    user: User = Depends(get_current_user),
    pg_db: Session = Depends(get_db),
):
    conversation = pg_db.query(Conversation).filter(
        Conversation.id == conv_id,
        Conversation.user_id == user.id,
    ).first()
    if not conversation:
        raise HTTPException(status_code=404, detail="对话不存在")
    pg_db.delete(conversation)
    pg_db.commit()
    return {"message": "删除成功"}


@router.patch("/conversations/{conv_id}", response_model=ConversationOut)
def update_conversation(
    conv_id: int,
    req: ConversationUpdate,
    user: User = Depends(get_current_user),
    pg_db: Session = Depends(get_db),
):
    conversation = pg_db.query(Conversation).filter(
        Conversation.id == conv_id,
        Conversation.user_id == user.id,
    ).first()
    if not conversation:
        raise HTTPException(status_code=404, detail="对话不存在")
    conversation.title = req.title
    pg_db.commit()
    return ConversationOut(
        id=conversation.id,
        title=conversation.title,
        created_at=conversation.created_at.isoformat() if conversation.created_at else "",
        updated_at=conversation.updated_at.isoformat() if conversation.updated_at else "",
        message_count=len(conversation.messages) if conversation.messages else 0,
    )


def _derive_title(current_title: str, message: str) -> str:
    if current_title and current_title != "新对话":
        return current_title
    return message[:30] + ("..." if len(message) > 30 else "")


def _extract_attraction_mentions(text: str) -> list[str]:
    """Extract attraction names mentioned in agent response."""
    import re
    names = set()
    # Match 《景点名》 or 【景点名】 patterns
    for m in re.finditer(r'[《【](.+?)[》】]', text):
        names.add(m.group(1))
    return list(names)
