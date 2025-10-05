from enum import Enum


from .base_enum import BaseEnum


class StudyType(BaseEnum):
    CASE_REPORT = "Case report"
    COMMENTARY = "Commentary"
    COMPARATIVE_GENOMICS = "Comparative genomics"
    COMPUTATIONAL_STUDY = "Computational study"
    DATA_REPOSITORY = "Data repository"
    DOSE_RESPONSE_STUDY = "Dose response study"
    EXPERIMENTAL_STUDY = "Experimental study"
    GENOMIC_ANALYSIS = "Genomic analysis"
    HARDWARE_VALIDATION = "Hardware validation"
    HYPOTHESIS_PAPER = "Hypothesis paper"
    IN_SILICO_STUDY = "In silico study"
    INTEGRATED_MULTI_OMICS = "Integrated multi-omics"
    LONGITUDINAL_STUDY = "Longitudinal study"
    MENDELIAN_RANDOMIZATION = "Mendelian randomization"
    META_ANALYSIS = "Meta analysis"
    METHOD_DEVELOPMENT = "Method development"
    OBSERVATIONAL_STUDY = "Observational study"
    PERSPECTIVE = "Perspective"
    PRECLINICAL_STUDY = "Preclinical study"
    PROTOCOL_DESCRIPTION = "Protocol description"
    QUANTITATIVE_NATURAL_VARIATION = "Quantitative natural variation"
    RANDOMIZED_CONTROLLED_TRIAL = "Randomized controlled trial"
    REANALYSIS = "Reanalysis"
    REPEATED_MEASURES_DESIGN = "Repeated measures design"
    REVIEW = "Review"
    SYSTEMS_BIOLOGY_STUDY = "Systems biology study"
    THEORETICAL_MODEL = "Theoretical model"
    TRANSLATIONAL_RESEARCH = "Translational research"
    VALIDATION_STUDY = "Validation study"