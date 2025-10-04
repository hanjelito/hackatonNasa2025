from app.dto.chat_request import ChatRequest
from app.dto.chat_message import ChatMessage


async def chat(request: ChatRequest) -> ChatMessage:
    """Genera la siguiente respuesta del asistente dado el historial de chat.

    TODO: Integrar llamada al modelo de lenguaje (Vertex AI u otro) usando el paper_id
    para contextualizar la respuesta con el contenido del paper.
    """
    # Estrategia provisional: responder eco-resumen del último mensaje del usuario
    last_user_msg = None
    for m in reversed(request.messages):
        if m.role == "user":
            last_user_msg = m
            break

    content = (
        "He recibido tu mensaje. (stub)\n\n"
        f"paper_id: {request.paper_id}\n"
        f"ultimo_mensaje_usuario: {last_user_msg.content if last_user_msg else 'N/A'}\n\n"
        "TODO: llamar al modelo para generar una respuesta contextualizada."
    )

    return ChatMessage(role="model", content=content)

