from fastapi import APIRouter, Query
from typing import Optional

from app.dto.chat_message import ChatMessage
from app.dto.chat_request import ChatRequest
from app.dto.chat_session_response import ChatSessionResponse
from app.services.chat_service import chat, get_chat_history, initialize_or_get_session

chat_router = APIRouter(
    prefix="/chat",
    tags=["Chat"],
)


@chat_router.get("/session/{paper_id}", response_model=ChatSessionResponse)
async def initialize_session_endpoint(
    paper_id: str,
    session_token: Optional[str] = Query(
        default=None,
        description="Token de sesión existente (opcional). Si se proporciona y es válido, recupera la sesión."
    )
):
    """
    Inicializa una nueva sesión de chat o recupera una existente.

    - Si no se proporciona session_token, crea una nueva sesión
    - Si se proporciona session_token y es válido (< 2 min sin actividad), recupera la sesión
    - Si el token expiró, crea una nueva sesión

    El frontend debe llamar a este endpoint cuando se abre el chat widget.
    """
    return await initialize_or_get_session(paper_id, session_token)


@chat_router.post("", response_model=ChatMessage)
async def chat_endpoint(chat_request: ChatRequest):
    """
    Envía un mensaje al chat. Requiere un session_token válido.
    """
    return await chat(chat_request)


@chat_router.get("/history/{paper_id}")
async def get_chat_history_endpoint(paper_id: str):
    """
    Obtiene el historial completo de chat para un paper específico.
    """
    return await get_chat_history(paper_id)

