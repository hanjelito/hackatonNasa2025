from json import loads
from app.config.vertexai_client import VertexAIClient
from app.config.settings import settings
from google.genai.types import GenerateContentConfig

vertex_ai_client = VertexAIClient()

# Prompt para estructurar datos del artículo científico
EXTRACTION_PROMPT = """
Extrae y estructura la siguiente información del texto científico en formato JSON:

{
  "authors": ["lista de autores"],
}

Responde ÚNICAMENTE con el JSON válido, sin texto adicional.
"""

async def extract_structured_data(text: str) -> dict:
    """
    Usa LLM para extraer datos estructurados del texto del artículo
    
    Args:
        text: Texto completo del artículo
        
    Returns:
        dict: Datos estructurados del artículo
    """

    response = vertex_ai_client.client.models.generate_content(
        model="cferfrfr",
        contents=text,
        config=GenerateContentConfig(
            system_instruction=EXTRACTION_PROMPT,
            temperature=0,
        ),
    )

    if not response.text:
        raise Exception("Vertex AI Error: No response text received")

    try:
        # Parsear la respuesta JSON
        structured_data = loads(response.text.strip())
        return structured_data
    except ValueError:
        raise Exception(f"Error parsing JSON response: {response.text}")


async def process_article(text: str) -> dict:
    """
    Función principal: extrae texto de HTML y lo estructura con LLM
    
    Args:
        html_content: Contenido HTML del artículo
        
    Returns:
        dict: Datos estructurados del artículo científico
    """
    
    structured_data = await extract_structured_data(text)
    
    return structured_data

