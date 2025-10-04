from enum import Enum


class SamplingMethod(Enum):
    RANDOM = "RANDOM"
    STRATIFIED = "STRATIFIED"
    CONVENIENCE = "CONVENIENCE"
    SNOWBALL = "SNOWBALL"
    SYSTEMATIC = "SYSTEMATIC"
