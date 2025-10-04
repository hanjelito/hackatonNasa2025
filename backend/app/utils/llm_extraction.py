import json
from app.config.vertexai_client import VertexAIClient
from app.config.settings import settings
from app.utils.extractor_articulo import ExtractorArticulo
from google.genai.types import GenerateContentConfig

vertex_ai_client = VertexAIClient()

# Prompt para estructurar datos del artículo científico
EXTRACTION_PROMPT = """
Extrae y estructura la siguiente información del texto científico en formato JSON:

{
  "title": "título del artículo",
  "abstract": "resumen/abstract del artículo",
  "authors": ["lista de autores"],
  "journal": "nombre de la revista",
  "publication_date": "fecha de publicación",
  "doi": "DOI si está disponible",
  "keywords": ["palabras clave extraídas"],
  "methodology": "descripción breve de la metodología",
  "main_findings": "principales hallazgos o resultados",
  "conclusions": "conclusiones principales"
}

Responde ÚNICAMENTE con el JSON válido, sin texto adicional.
"""


def extract_text_from_html(html_content: str) -> str:
    """
    Extrae texto limpio de contenido HTML usando ExtractorArticulo
    
    Args:
        html_content: Contenido HTML del artículo
        
    Returns:
        str: Texto completo extraído y limpio
    """
    from bs4 import BeautifulSoup

    extractor = ExtractorArticulo()
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Extraer componentes del artículo
    title = extractor.extraer_titulo(soup)
    abstract = extractor.extraer_abstract(soup)
    content = extractor.extraer_contenido_principal(soup)
    
    # Combinar todo el texto
    full_text = f"Title: {title}\n\n"
    if abstract:
        full_text += f"Abstract: {abstract}\n\n"
    full_text += f"Content: {content}"
    
    return full_text


async def extract_structured_data(text: str) -> dict:
    """
    Usa LLM para extraer datos estructurados del texto del artículo
    
    Args:
        text: Texto completo del artículo
        
    Returns:
        dict: Datos estructurados del artículo
    """
    response = vertex_ai_client.client.models.generate_content(
        model="gemini-2.5-flash-lite",
        contents=text,
        config=GenerateContentConfig(
            system_instruction=EXTRACTION_PROMPT,
            temperature=0,
        )
    )

    if not response.text:
        raise Exception("Vertex AI Error: No response text received")
    
    try:
        # Parsear la respuesta JSON
        structured_data = json.loads(response.text.strip())
        return structured_data
    except json.JSONDecodeError:
        raise Exception(f"Error parsing JSON response: {response.text}")


async def process_article(html_content: str) -> dict:
    """
    Función principal: extrae texto de HTML y lo estructura con LLM
    
    Args:
        html_content: Contenido HTML del artículo
        
    Returns:
        dict: Datos estructurados del artículo científico
    """
    # 1. Extraer texto limpio del HTML
    text = extract_text_from_html(html_content)
    
    # 2. Estructurar datos con LLM
    structured_data = await extract_structured_data(text)
    
    return structured_data

