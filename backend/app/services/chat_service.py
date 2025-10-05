from app.dto.chat_request import ChatRequest
from app.dto.chat_message import ChatMessage
from app.dto.chat_session_response import ChatSessionResponse
from app.config.vertexai_client import VertexAIClient
from app.config.settings import settings
from app.utils.prompt_loader import PromptLoader
from app.models.paper import Paper
from app.models.chat import ChatHistory
from beanie import PydanticObjectId
from google.genai import types
from google.genai.types import GenerateContentConfig
from fastapi import HTTPException
from datetime import datetime, timezone, timedelta
import uuid


async def chat(request: ChatRequest) -> ChatMessage:
    # Intentar obtener el paper de la base de datos si es un ObjectId válido
    paper = None
    paper_text = ""

    try:
        paper_id = PydanticObjectId(request.paper_id)
        paper = await Paper.get(paper_id)
        if paper:
            paper_text = (paper.full_text or "").strip()
    except Exception:
        # Si no es un ObjectId válido, continuar sin paper (para IDs mock)
        pass

    # Si no hay paper o no tiene texto, usar un texto por defecto
    if not paper_text:
        paper_text = f"Este es un artículo de investigación científica sobre exploración espacial (ID: {request.paper_id}). No se encontró el texto completo en la base de datos."

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

    # Validar que se proporcione session_token
    if not request.session_token:
        raise HTTPException(
            status_code=400,
            detail="Se requiere session_token. Primero inicializa una sesión con GET /chat/session/{paper_id}"
        )

    # Guardar todo el historial de chat en la base de datos
    await save_chat_history(request.paper_id, request.session_token, request.messages, content)

    return ChatMessage(role="model", content=content)


async def initialize_or_get_session(paper_id: str, session_token: str = None) -> ChatSessionResponse:
    """
    Inicializa una nueva sesión de chat o recupera una existente.

    - Si se proporciona session_token y es válido (< 2 min sin actividad), recupera la sesión
    - Si el token expiró o no existe, crea una nueva sesión
    - Si no se proporciona token, crea una nueva sesión
    """
    SESSION_TIMEOUT_MINUTES = 2

    # Si se proporciona un token, intentar recuperar la sesión
    if session_token:
        chat_history = await ChatHistory.find_one(
            ChatHistory.session_token == session_token,
            ChatHistory.paper_id == paper_id
        )

        if chat_history:
            # Verificar si la sesión aún está activa (< 2 min sin actividad)
            # Asegurar que last_activity tenga timezone
            last_activity = chat_history.last_activity
            if last_activity.tzinfo is None:
                last_activity = last_activity.replace(tzinfo=timezone.utc)

            time_since_activity = datetime.now(timezone.utc) - last_activity

            if time_since_activity < timedelta(minutes=SESSION_TIMEOUT_MINUTES):
                # Sesión válida, actualizar última actividad
                chat_history.last_activity = datetime.now(timezone.utc)
                await chat_history.save()

                return ChatSessionResponse(
                    session_token=chat_history.session_token,
                    paper_id=chat_history.paper_id,
                    messages=chat_history.messages,
                    is_new_session=False,
                    last_activity=chat_history.last_activity
                )

    # Crear nueva sesión
    new_session_token = str(uuid.uuid4())
    chat_history = ChatHistory(
        paper_id=paper_id,
        session_token=new_session_token,
        messages=[],
        last_activity=datetime.now(timezone.utc),
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc)
    )
    await chat_history.insert()

    return ChatSessionResponse(
        session_token=new_session_token,
        paper_id=paper_id,
        messages=[],
        is_new_session=True,
        last_activity=chat_history.last_activity
    )


async def save_chat_history(paper_id: str, session_token: str, user_messages: list, model_response: str):
    """
    Guarda el historial de chat en la base de datos para una sesión específica.
    Actualiza la última actividad de la sesión.
    """
    SESSION_TIMEOUT_MINUTES = 2

    # Buscar la sesión por token y paper_id
    chat_history = await ChatHistory.find_one(
        ChatHistory.session_token == session_token,
        ChatHistory.paper_id == paper_id
    )

    if not chat_history:
        raise HTTPException(status_code=404, detail="Sesión no encontrada o expirada")

    # Verificar si la sesión expiró
    # Asegurar que last_activity tenga timezone
    last_activity = chat_history.last_activity
    if last_activity.tzinfo is None:
        last_activity = last_activity.replace(tzinfo=timezone.utc)

    time_since_activity = datetime.now(timezone.utc) - last_activity
    if time_since_activity >= timedelta(minutes=SESSION_TIMEOUT_MINUTES):
        raise HTTPException(status_code=410, detail="Sesión expirada. Por favor, inicia una nueva sesión.")

    # Convertir todos los mensajes a un formato consistente con timestamp
    all_messages = []

    # Agregar todos los mensajes del usuario
    for msg in user_messages:
        all_messages.append({
            "role": msg.role,
            "content": msg.content,
            "timestamp": datetime.now(timezone.utc)
        })

    # Agregar la respuesta del modelo
    all_messages.append({
        "role": "model",
        "content": model_response,
        "timestamp": datetime.now(timezone.utc)
    })

    # Actualizar el historial agregando los nuevos mensajes
    chat_history.messages.extend(all_messages)
    chat_history.last_activity = datetime.now(timezone.utc)
    chat_history.updated_at = datetime.now(timezone.utc)
    await chat_history.save()


async def get_chat_history(paper_id: str):
    """
    Obtiene el historial completo de chat para un paper específico.
    """
    chat_history = await ChatHistory.find_one(ChatHistory.paper_id == paper_id)

    if chat_history is None:
        return {"paper_id": paper_id, "messages": [], "created_at": None, "updated_at": None}

    return {
        "paper_id": str(chat_history.paper_id),
        "messages": chat_history.messages,
        "created_at": chat_history.created_at,
        "updated_at": chat_history.updated_at
    }
