from typing import List, Optional

from pydantic import BaseModel, Field

from app.dto.chat_message import ChatMessage


class ChatRequest(BaseModel):

    paper_id: str
    session_token: Optional[str] = Field(
        default=None,
        description="Token de sesión para mantener la conversación. Si no se proporciona, se creará una nueva sesión."
    )
    messages: List[ChatMessage] = Field(
        default_factory=list,
        min_length=1,
        description="Historial de mensajes en orden cronológico",
    )

    class Config:
        json_schema_extra = {
            "example": {
                "paper_id": "67003efb4c2e3f7a9c2b5a11",
                "session_token": "550e8400-e29b-41d4-a716-446655440000",
                "messages": [
                    {
                        "role": "model",
                        "content": "El paper trata sobre..."
                    },
                    {
                        "role": "user",
                        "content": "Resume el paper y menciona sus conclusiones principales."
                    }
                ]
            }
        }
        from_attributes = True