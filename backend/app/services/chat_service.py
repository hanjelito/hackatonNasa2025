from app.dto.chat_request import ChatRequest
from app.dto.chat_message import ChatMessage
from app.config.vertexai_client import VertexAIClient
from app.config.settings import settings
from app.utils.prompt_loader import PromptLoader
from google.genai import types
from google.genai.types import GenerateContentConfig
from fastapi import HTTPException


async def chat(request: ChatRequest) -> ChatMessage:
    client = VertexAIClient().client
    prompr_loader = PromptLoader()
    # Cargar prompt de sistema y renderizar con el texto del paper (mock por ahora)

    # TODO: Obtener el texto real del paper por request.paper_id desde la base de datos o servicio
    mock_paper_text = (
        "De momento actua como un experto en biología molecular que ha leído el siguiente paper: Biology in the 21st Century."
        f"paper_id={request.paper_id}"
    )
    system_prompt = prompr_loader.render("chat_system_biology_paper_expert", {"paper_text": mock_paper_text})

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
        config=GenerateContentConfig(
            system_instruction=system_prompt,
        ),
    )

    content = getattr(response, "text", None)
    if not content or not str(content).strip():
        raise HTTPException(status_code=502, detail="Vertex AI no devolvió contenido.")

    return ChatMessage(role="model", content=content)
