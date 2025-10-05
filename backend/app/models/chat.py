from beanie import Document
from typing import List, Optional
from datetime import datetime, timezone
from pydantic import Field
import uuid


class ChatHistory(Document):
    """
    Modelo para guardar el historial completo de chats de un paper.
    Cada documento representa una sesión de chat específica con un token único.
    """

    paper_id: str = Field(description="ID del paper al que pertenece este chat")

    session_token: str = Field(
        default_factory=lambda: str(uuid.uuid4()),
        description="Token único de sesión para identificar esta conversación"
    )

    messages: List[dict] = Field(
        default_factory=list,
        description="Lista de mensajes con estructura: {role: 'user'|'model', content: str, timestamp: datetime}"
    )

    last_activity: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="Última vez que hubo actividad en esta sesión"
    )

    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Settings:
        name = "chat_histories"
        indexes = [
            "paper_id",
            "session_token",  # Índice para buscar por token de sesión
        ]
