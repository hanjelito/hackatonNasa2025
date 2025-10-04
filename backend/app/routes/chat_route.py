from fastapi import APIRouter

from app.dto.chat_message import ChatMessage
from app.dto.chat_request import ChatRequest
from app.services.chat_service import chat

chat_router = APIRouter(
    prefix="/chat",
    tags=["Chat"],
)


@chat_router.post("", response_model=ChatMessage)
async def chat_endpoint(chat_request: ChatRequest):
    return await chat(chat_request)

