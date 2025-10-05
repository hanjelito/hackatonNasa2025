from app.dto.chat_request import ChatRequest
from app.dto.chat_message import ChatMessage
from app.config.vertexai_client import VertexAIClient
from app.config.settings import settings
from app.utils.prompt_loader import PromptLoader
from app.models.paper import Paper
from beanie import PydanticObjectId
from google.genai import types
from google.genai.types import GenerateContentConfig
from fastapi import HTTPException


async def chat(request: ChatRequest) -> ChatMessage:
    # Obtener el paper y validar que tiene full_text
    try:
        paper_id = PydanticObjectId(request.paper_id)
    except Exception:
        raise HTTPException(status_code=400, detail="paper_id inválido")

    paper = await Paper.get(paper_id)
    if paper is None:
        raise HTTPException(status_code=404, detail="Paper no encontrado")

    paper_text = (paper.full_text or "").strip()
    if not paper_text:
        raise HTTPException(status_code=422, detail="El paper no tiene full_text disponible")

    # Cargar prompt de sistema y renderizar con el texto del paper
    loader = PromptLoader()
    system_prompt = loader.render("chat_system_biology_paper_expert", {"paper_text": paper_text})

    # Construye los contenidos usando los objetos oficiales de la SDK (types.Content/Part)
    contents = [
        types.Content(
            role=m.role,
            parts=[types.Part.from_text(text=m.content)],
        )
        for m in request.messages
    ]

    client = VertexAIClient().client
    response = client.models.generate_content(
        model=settings.VERTEXAI_MODEL_NAME,
        contents=contents,
        config=GenerateContentConfig(
            system_instruction=system_prompt,
        ),
    )

    # Extraer el texto de la respuesta y validar que no esté vacío
    content = getattr(response, "text", None)
    if not content or not str(content).strip():
        raise HTTPException(status_code=502, detail="Vertex AI no devolvió contenido.")

    return ChatMessage(role="model", content=content)
