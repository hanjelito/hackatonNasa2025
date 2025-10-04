from beanie import Document
from typing import List


class Paper(Document):
    id: str
    title: str
    description: str
    date: str
    source: str
    year: int
    organism: str
    authors: List[str]
    imageUrl: str

    class Settings:
        name = "papers"

    class Config:
        schema_extra = {
            "example": {
                "id": "1",
                "title": "Mars Rover Discovers Ancient Water Evidence",
                "description": "NASA's Perseverance rover has found compelling evidence of ancient water flows on Mars, suggesting the planet may have once supported microbial life.",
                "date": "2025-09-15",
                "source": "NASA Mars Exploration",
                "year": 2025,
                "organism": "NASA",
                "authors": ["Dr. Sarah Martinez", "Dr. James Chen", "Dr. Emily Rodriguez"],
                "imageUrl": "https://images-assets.nasa.gov/image/PIA25731/PIA25731~medium.jpg"
            }
        }