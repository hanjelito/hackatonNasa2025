from beanie import Document
from typing import List, Optional
from datetime import datetime

from .enums.organism import Organism
from .enums.study_type import StudyType
from .enums.experimental_platform import ExperimentalPlatform
from .enums.stressor import Stressor
from .enums.organ import Organ
from .enums.analysis_level import AnalysisLevel
from .enums.sampling_method import SamplingMethod
from .enums.health_implications_severity import HealthImplicationsSeverity
from .enums.space_agency import SpaceAgency
from .enums.applicable_mission import ApplicableMission


class Paper(Document):
    # Identificación básica del paper
    title: str # HECHO
    pmcid: str = "" 
    doi: str = ""
    pubmed_url: str = ""
    publication_date: Optional[datetime] = None
    journal_name: str = ""
    image_url: str = "https://images-assets.nasa.gov/image/PIA25731/PIA25731~medium.jpg"
    
    # Contenido del paper
    abstract: str = ""
    full_text: str = ""
    conclusion: str = "" # HECHO
    
    # Autoría y procedencia
    authors: List[str] = [] # PEDIR
    author_affiliations: List[str] = [] # PEDIR
    
    # Resumen semántico (para búsquedas)
    ai_generated_summary: str = "" # HECHO
    key_findings: str = "" # HECHO
    future_research_fields: str = "" # HECHO
    impact_statement: str = ""  # HECHO
    
    # Clasificación del estudio
    study_type: Optional[StudyType] = None # PEDIR
    experimental_platform: Optional[ExperimentalPlatform] = None # PEDIR
    space_environment_stressors: List[Stressor] = [] # PEDIR
    related_papers: List[str] = []  # HECHO

    # Sujetos de estudio biológico
    primary_organisms_studied: List[Organism] = [] # PEDIR
    affected_organ_systems: List[Organ] = []  # PEDIR
    biological_analysis_level: List[AnalysisLevel] = []  # PEDIR
    
    # Metodología
    experimental_duration_days: Optional[int] = None  # PEDIR
    sample_size: Optional[int] = None   # PEDIR
    sampling_methodology: Optional[SamplingMethod] = None # PEDIR
    
    # Resultados y relevancia espacial
    demonstrates_space_adaptation: bool = False  # PEDIR
    identifies_countermeasures: bool = False  # PEDIR
    relevant_for_long_duration_missions: bool = False  # PEDIR
    health_implications_severity: Optional[HealthImplicationsSeverity] = None # PEDIR
    reproducibility_level: Optional[str] = None # HECHO 

    # Misiones y aplicabilidad
    applicable_to_missions: List[ApplicableMission] = []  # PEDIR
    space_agency_involvement: List[SpaceAgency] = []  # PEDIR
    
    class Settings:
        name = "papers"