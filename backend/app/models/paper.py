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
    title: Optional[str] = None
    pmcid: Optional[str] = None
    doi: Optional[str] = None
    pubmed_url: Optional[str] = None
    publication_date: Optional[datetime] = None
    journal_name: Optional[str] = None

    # Contenido del paper
    abstract: Optional[str] = None
    full_text: Optional[str] = None

    # Autoría y procedencia
    authors: Optional[List[str]] = None
    author_affiliations: Optional[List[str]] = None

    # Resumen semántico (para búsquedas)
    ai_generated_summary: Optional[str] = None
    key_findings: Optional[str] = None
    clinical_relevance: Optional[str] = None

    # Clasificación del estudio
    study_type: Optional[StudyType] = None
    experimental_platform: Optional[ExperimentalPlatform] = None
    space_environment_stressors: Optional[List[Stressor]] = None  # Qué factores espaciales se estudian

    # Sujetos de estudio biológico
    primary_organisms_studied: Optional[List[Organism]] = None
    affected_organ_systems: Optional[List[Organ]] = None  # Qué sistemas del cuerpo se afectan
    biological_analysis_level: Optional[List[AnalysisLevel]] = None  # Celular, molecular, etc.

    # Metodología
    experimental_duration_days: Optional[int] = None  # Duración del experimento
    sample_size: Optional[int] = None  # Número de sujetos/muestras
    sampling_methodology: Optional[SamplingMethod] = None
    analytical_methods_used: Optional[List[AnalysisMethod]] = None

    # Tecnologías y técnicas específicas
    molecular_techniques: Optional[List[str]] = None  # RNA-seq, proteómica, etc.
    measurement_technologies: Optional[List[str]] = None  # Microscopía, espectrómetros, etc.

    # Resultados y relevancia espacial
    demonstrates_space_adaptation: Optional[bool] = None  # Si muestra adaptación al espacio
    identifies_countermeasures: Optional[bool] = None  # Si propone contramedidas
    relevant_for_long_duration_missions: Optional[bool] = None  # Mars, Luna, etc.
    health_implications_severity: Optional[str] = None  # LOW, MODERATE, HIGH, CRITICAL

    # Misiones y aplicabilidad
    applicable_to_missions: Optional[List[str]] = None  # ISS, Artemis, Mars, etc.
    space_agency_involvement: Optional[List[str]] = None  # NASA, ESA, JAXA, etc.

    # Metadatos de procesamiento
    extraction_confidence_score: Optional[float] = None  # Confianza en la extracción automática
    requires_human_review: Optional[bool] = None
    tags: Optional[List[str]] = None  # Para categorización flexible

    class Settings:
        name = "papers"