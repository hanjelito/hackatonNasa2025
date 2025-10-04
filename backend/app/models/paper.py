from beanie import Document


class Paper(Document):
    prueba: str

    class Settings:
            name = "papers"