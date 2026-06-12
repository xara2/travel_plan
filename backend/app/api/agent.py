"""AI Agent autonomous planning endpoints."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..utils.auth import get_current_user
from ..models.user import User
from ..models.conversation import Conversation, Message
from ..agent.react_agent import ReActAgent, ConversationMemory

router = APIRouter(prefix="/api/agent", tags=["agent"])


@router.post("/plan")
async def run_agent_plan(
    destination: str,
    duration: int = 3,
    preferences: str = "",
    user: User = Depends(get_current_user),
    pg_db: Session = Depends(get_db),
):
    """Autonomous AI plan generation: search attractions → generate itinerary."""
    prompt = f"帮我在{destination}规划一个{duration}天的旅行计划"
    if preferences:
        prompt += f"，我的偏好：{preferences}"
    prompt += "。请先搜索当地的景点，然后根据搜索结果生成每天的行程安排。"

    agent = ReActAgent()

    conversation = Conversation(
        user_id=user.id,
        title=f"{destination}{duration}天旅行计划",
    )
    pg_db.add(conversation)
    pg_db.flush()

    user_msg = Message(
        conversation_id=conversation.id,
        role="user",
        content=prompt,
    )
    pg_db.add(user_msg)
    pg_db.flush()

    conversation = pg_db.query(Conversation).filter(
        Conversation.id == conversation.id,
    ).first()
    memory = ConversationMemory(conversation)

    response = await agent.run(memory, prompt)

    assistant_msg = Message(
        conversation_id=conversation.id,
        role="assistant",
        content=response,
    )
    pg_db.add(assistant_msg)
    pg_db.commit()

    return {
        "conversation_id": conversation.id,
        "plan": response,
    }


@router.get("/plan/{conv_id}/status")
def get_plan_status(
    conv_id: int,
    user: User = Depends(get_current_user),
    pg_db: Session = Depends(get_db),
):
    """Check the status/results of an agent planning task."""
    conversation = pg_db.query(Conversation).filter(
        Conversation.id == conv_id,
        Conversation.user_id == user.id,
    ).first()
    if not conversation:
        raise HTTPException(status_code=404, detail="任务不存在")

    messages = sorted(conversation.messages, key=lambda m: m.created_at or "")
    return {
        "conversation_id": conversation.id,
        "status": "completed" if messages else "running",
        "messages": [
            {"role": m.role, "content": m.content[:200]}
            for m in messages
        ],
    }
