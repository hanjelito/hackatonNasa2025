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
    title: str
    pmcid: str = "" 
    doi: str = ""
    pubmed_url: str = ""
    publication_date: Optional[datetime] = None
    journal_name: str = ""
    image_url: str = "https://images-assets.nasa.gov/image/PIA25731/PIA25731~medium.jpg"
    
    # Contenido del paper
    abstract: str = ""
    full_text: str = ""
    conclusion: str = ""
    
    # Autoría y procedencia
    authors: List[str] = []
    author_affiliations: List[str] = []
    
    # Resumen semántico (para búsquedas)
    ai_generated_summary: str = ""
    key_findings: str = ""
    future_research_fields: str = ""
    impact_statement: str = "" 
    
    # Clasificación del estudio
    study_type: Optional[StudyType] = None
    experimental_platform: Optional[ExperimentalPlatform] = None
    space_environment_stressors: List[Stressor] = []
    related_papers: List[str] = [] 

    # Sujetos de estudio biológico
    primary_organisms_studied: List[Organism] = []
    affected_organ_systems: List[Organ] = []
    biological_analysis_level: List[AnalysisLevel] = []
    
    # Metodología
    experimental_duration_days: Optional[int] = None
    sample_size: Optional[int] = None 
    sampling_methodology: Optional[SamplingMethod] = None
    
    # Resultados y relevancia espacial
    demonstrates_space_adaptation: bool = False
    identifies_countermeasures: bool = False
    relevant_for_long_duration_missions: bool = False
    health_implications_severity: Optional[HealthImplicationsSeverity] = None
    reproducibility_level: Optional[str] = None 

    # Misiones y aplicabilidad
    applicable_to_missions: List[ApplicableMission] = []
    space_agency_involvement: List[SpaceAgency] = []
    
    class Settings:
        name = "papers"