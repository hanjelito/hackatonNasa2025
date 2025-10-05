from typing import Optional
from pydantic import BaseModel
from app.dto.filter_value import FilterValue

class SearchPapersRequest(BaseModel):
    query: Optional[str] = None
    filters: Optional[list[FilterValue]] = None
    limit: Optional[int] = 10

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "query": "Cancer immunotherapy",
                "filters":
                    [
                        {
                            "name": "primary_organisms_studied",
                            "values": ["Homo sapiens", "Danio rerio", "Mus musculus"]
                        },
                        {
                            "name": "study_type",
                            "values": ["Review"]
                        }
                    ],
                "limit": 15
            }
        }
