from typing import Literal

from pydantic import BaseModel, Field


class ChatMessage(BaseModel):

    role: Literal["user", "model"]
    content: str = Field(min_length=1, description="Texto del mensaje")

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "role": "model",
                "content": "¿Qué efectos provoca la microgravedad en el sistema cardiovascular?"
            }
        }
