from app.dto.chat_request import ChatRequest
from app.dto.chat_message import ChatMessage
from app.config.vertexai_client import VertexAIClient
from app.config.settings import settings
from google.genai import types
from fastapi import HTTPException


async def chat(request: ChatRequest) -> ChatMessage:
    client = VertexAIClient().client

    # Construye los contenidos usando los objetos oficiales de la SDK (types.Content/Part)
    contents = [
        types.Content(
            role=m.role,
            parts=[types.Part.from_text(text=m.content)],
        )
        for m in request.messages
    ]

    response = client.models.generate_content(
        model=settings.VERTEXAI_MODEL_NAME,
        contents=contents,
    )

    content = getattr(response, "text", None)
    if not content or not str(content).strip():
        raise HTTPException(status_code=502, detail="Vertex AI no devolvió contenido.")

    return ChatMessage(role="model", content=content)
