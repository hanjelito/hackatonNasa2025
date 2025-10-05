from .base_enum import BaseEnum


class HealthImplicationsSeverity(BaseEnum):
    CRITICAL = "Critical"
    HIGH = "High"
    MODERATE = "Moderate"
    LOW = "Low"