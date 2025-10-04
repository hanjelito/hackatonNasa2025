from json import loads
from app.config.vertexai_client import VertexAIClient
from google.genai.types import GenerateContentConfig
from app.config.settings import settings


vertex_ai_client = VertexAIClient()

# Prompt para estructurar datos del artículo científico
EXTRACTION_PROMPT = """
Extract and structure the following information from this space biology/life sciences research paper in JSON format.

For each field, extract the most accurate information possible from the text. If information is not available, use empty string, empty array, or null as appropriate.

{
  "title": "Full title of the paper",
  "pmcid": "PubMed Central ID if mentioned (e.g., PMC10020673)",
  "doi": "Digital Object Identifier if mentioned",
  "journal_name": "Name of the journal where published",
  "authors": ["List of all authors mentioned"],
  "author_affiliations": ["List of institutions/universities mentioned for authors"],
  
  "ai_generated_summary": "Write a concise 2-3 sentence summary of the main research focus",
  "key_findings": "Summarize the most important results and discoveries",
  "clinical_relevance": "Explain the potential medical/health implications for space missions",
  
  "study_type": "Type of study conducted (e.g., experimental, observational, longitudinal, case study, etc.)",
  "experimental_platform": "Where the study was conducted (e.g., International Space Station, ground-based simulation, parabolic flight, etc.)",
  "space_environment_stressors": ["List all space-related factors studied (e.g., microgravity, radiation, isolation, etc.)"],
  
  "primary_organisms_studied": ["List all organisms studied (e.g., human, mouse, rat, plants, microorganisms, cells, etc.)"],
  "affected_organ_systems": ["List body systems affected (e.g., musculoskeletal, cardiovascular, immune, nervous, etc.)"],
  "biological_analysis_level": ["Level of biological analysis (e.g., molecular, cellular, tissue, organ, organism level)"],
  
  "experimental_duration_days": "Duration of the experiment in days (number only, null if not specified)",
  "sample_size": "Number of subjects/samples studied (number only, null if not specified)",
  "sampling_methodology": "How samples were collected/selected (e.g., random, stratified, convenience sampling)",
  "analytical_methods_used": ["Statistical or analytical methods used (e.g., ANOVA, regression, descriptive analysis, etc.)"],
  
  "molecular_techniques": ["Specific molecular/biochemical techniques used (e.g., RNA sequencing, proteomics, PCR, Western blot, etc.)"],
  "measurement_technologies": ["Instruments and technologies used for measurements (e.g., microscopy, spectroscopy, MRI, etc.)"],
  
  "demonstrates_space_adaptation": "true/false - Does the study show biological adaptation to space environment?",
  "identifies_countermeasures": "true/false - Does the study propose interventions/countermeasures for space-related health issues?",
  "relevant_for_long_duration_missions": "true/false - Are findings relevant for long-duration space missions (Mars, Moon, etc.)?",
  "health_implications_severity": "Assess severity of health implications (LOW, MODERATE, HIGH, CRITICAL)",
  
  "applicable_to_missions": ["List space missions this research applies to (e.g., ISS, Artemis, Mars missions, etc.)"],
  "space_agency_involvement": ["Space agencies involved or mentioned (e.g., NASA, ESA, JAXA, etc.)"],
  
  "tags": ["Generate 5-10 relevant tags for categorization (e.g., bone loss, muscle atrophy, gene expression, etc.)"]
}

Respond ONLY with valid JSON, no additional text.
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
        model=settings.VERTEXAI_MODEL_NAME,
        contents=text,
        config=GenerateContentConfig(
            system_instruction=EXTRACTION_PROMPT,
            temperature=0,
            response_mime_type="application/json",
        )
        ,
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

