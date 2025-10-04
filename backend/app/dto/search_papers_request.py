from pydantic import BaseModel
from app.dto.filter_value import FilterValue

class SearchPapersRequest(BaseModel):
    query: str
    filters: list[FilterValue]
    limit: int = 10

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "query": "Cancer immunotherapy",
                "filters":
                    [
                        {"name": "organisms",
                         "values": ["Human", "Nematode", "Yeast"]
                         },
                        {"name": "article_types",
                         "values": ["Review", "Research Article"]
                         }
                    ]
            }
        }
