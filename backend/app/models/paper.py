from beanie import Document
from typing import List, Optional
from datetime import datetime

from .enums.organism import Organism
from .enums.study_type import StudyType
from .enums.experimental_platform import ExperimentalPlatform
from .enums.stressor import Stressor
from .enums.analysis_method import AnalysisMethod
from .enums.organ import Organ
from .enums.analysis_level import AnalysisLevel
from .enums.sampling_method import SamplingMethod


class Paper(Document):
    # Identificación básica del paper
    title: str
    pmcid: str = ""
    doi: str = ""
    pubmed_url: str = ""
    publication_date: Optional[datetime] = None
    journal_name: str = ""
    
    # Contenido del paper
    abstract: str = ""
    full_text: str = ""
    
    # Autoría y procedencia
    authors: List[str] = []
    author_affiliations: List[str] = []
    
    # Resumen semántico (para búsquedas)
    ai_generated_summary: str = ""
    key_findings: str = ""
    clinical_relevance: str = ""
    
    # Clasificación del estudio
    study_type: Optional[StudyType] = None
    experimental_platform: Optional[ExperimentalPlatform] = None
    space_environment_stressors: List[Stressor] = []  # Qué factores espaciales se estudian
    
    # Sujetos de estudio biológico
    primary_organisms_studied: List[Organism] = []
    affected_organ_systems: List[Organ] = []  # Qué sistemas del cuerpo se afectan
    biological_analysis_level: List[AnalysisLevel] = []  # Celular, molecular, etc.
    
    # Metodología
    experimental_duration_days: Optional[int] = None  # Duración del experimento
    sample_size: Optional[int] = None  # Número de sujetos/muestras
    sampling_methodology: Optional[SamplingMethod] = None
    analytical_methods_used: List[AnalysisMethod] = []
    
    # Tecnologías y técnicas específicas
    molecular_techniques: List[str] = []  # RNA-seq, proteómica, etc.
    measurement_technologies: List[str] = []  # Microscopía, espectrómetros, etc.
    
    # Resultados y relevancia espacial
    demonstrates_space_adaptation: bool = False  # Si muestra adaptación al espacio
    identifies_countermeasures: bool = False  # Si propone contramedidas
    relevant_for_long_duration_missions: bool = False  # Mars, Luna, etc.
    health_implications_severity: str = ""  # LOW, MODERATE, HIGH, CRITICAL
    
    # Misiones y aplicabilidad
    applicable_to_missions: List[str] = []  # ISS, Artemis, Mars, etc.
    space_agency_involvement: List[str] = []  # NASA, ESA, JAXA, etc.
    
    # Metadatos de procesamiento
    extraction_confidence_score: float = 0.0  # Confianza en la extracción automática
    requires_human_review: bool = True
    tags: List[str] = []  # Para categorización flexible

    class Settings:
        name = "papers"