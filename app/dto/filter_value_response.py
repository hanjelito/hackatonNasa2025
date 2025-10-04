from pydantic import BaseModel


class FilterValueResponse(BaseModel):
    name: str
    values: list[str]

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "name": "organisms",
                "values": [
                    "Human",
                    "Mouse",
                    "Rat",
                    "Zebrafish",
                    "Fruit fly",
                    "Nematode"
                    "Yeast"
                ]
            }
        }
