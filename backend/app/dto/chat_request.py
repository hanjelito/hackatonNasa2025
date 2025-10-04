from typing import List

from pydantic import BaseModel, Field

from app.dto.chat_message import ChatMessage


class ChatRequest(BaseModel):

    paper_id: str
    messages: List[ChatMessage] = Field(
        default_factory=list,
        min_length=1,
        description="Historial de mensajes en orden cronológico",
    )

    class Config:
        json_schema_extra = {
            "example": {
                "paper_id": "67003efb4c2e3f7a9c2b5a11",
                "messages": [
                    {
                        "role": "assistant",
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

