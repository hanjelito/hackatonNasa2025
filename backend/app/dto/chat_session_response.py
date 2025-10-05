from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class ChatSessionResponse(BaseModel):
    """
    Respuesta al inicializar o recuperar una sesión de chat.
    """

    session_token: str = Field(description="Token único de la sesión")
    paper_id: str = Field(description="ID del paper")
    messages: List[dict] = Field(
        default_factory=list,
        description="Historial de mensajes de la sesión"
    )
    is_new_session: bool = Field(description="True si es una sesión nueva, False si se recuperó una existente")
    last_activity: Optional[datetime] = Field(
        default=None,
        description="Última actividad de la sesión"
    )

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "session_token": "550e8400-e29b-41d4-a716-446655440000",
                "paper_id": "1",
                "messages": [],
                "is_new_session": True,
                "last_activity": "2025-10-05T12:00:00Z"
            }
        }
