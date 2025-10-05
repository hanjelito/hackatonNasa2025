from enum import Enum
from typing import Optional, List


class BaseEnum(str, Enum):
    """
    Base Enum class for all space biology enums.
    
    Inherits from str to make enum values JSON serializable and LLM-friendly.
    Provides utility methods for working with LLM outputs.
    """
    
    @classmethod
    def from_string(cls, value: str) -> Optional['BaseEnum']:
        """
        Create an enum instance from a string value (case-insensitive).
        Returns None if the value doesn't match any enum member.
        
        Args:
            value: String value to convert to enum
            
        Returns:
            Enum member or None if not found
        """
        if not value:
            return None
            
        # Try exact match first
        try:
            return cls(value)
        except ValueError:
            pass
        
        # Try case-insensitive match
        value_lower = value.lower().strip()
        for member in cls:
            if member.value.lower() == value_lower:
                return member
            if member.name.lower() == value_lower:
                return member
        
        return None
    
    @classmethod
    def from_string_list(cls, values: List[str]) -> List['BaseEnum']:
        """
        Convert a list of strings to a list of enum members.
        Skips invalid values.
        
        Args:
            values: List of string values to convert
            
        Returns:
            List of valid enum members
        """
        if not values:
            return []
        
        result = []
        for value in values:
            enum_value = cls.from_string(value)
            if enum_value:
                result.append(enum_value)
        
        return result
    
    @classmethod
    def all_values(cls) -> List[str]:
        """
        Get all possible enum values as strings.
        Useful for providing to LLMs as valid options.
        
        Returns:
            List of all enum value strings
        """
        return [member.value for member in cls]
    
    @classmethod
    def all_names(cls) -> List[str]:
        """
        Get all possible enum names.
        Useful for providing to LLMs as valid options.
        
        Returns:
            List of all enum names
        """
        return [member.name for member in cls]
    
    @classmethod
    def to_prompt_string(cls) -> str:
        """
        Generate a formatted string of all enum values for LLM prompts.
        
        Returns:
            Formatted string listing all valid enum values
        """
        values = cls.all_values()
        return f"Valid values: {', '.join(values)}"
    
    @classmethod
    def to_json_schema(cls) -> dict:
        """
        Generate a JSON schema enum definition for this enum.
        Useful for LLM structured outputs.
        
        Returns:
            JSON schema dict with enum values
        """
        return {
            "type": "string",
            "enum": cls.all_values(),
            "description": f"One of: {', '.join(cls.all_values())}"
        }
    
    def __str__(self) -> str:
        """Return the enum value as string"""
        return self.value
    
    def __repr__(self) -> str:
        """Return a readable representation"""
        return f"{self.__class__.__name__}.{self.name}"