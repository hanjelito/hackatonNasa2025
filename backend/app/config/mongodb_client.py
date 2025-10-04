from beanie import init_beanie, Document
from motor.motor_asyncio import AsyncIOMotorClient
from typing import List, Optional, Type


class MongoDbClient:
    def __init__(self, url: str, database_name: str = "hackaton_nasa_db", models: Optional[List[Type[Document]]] = None):
        # Lista de modelos Beanie (Document). Puede pasarse desde fuera.
        self.models: List[Type[Document]] = models or []
        self.client = AsyncIOMotorClient(url)
        self.database_name = database_name

    async def init(self):
        # Inicializa Beanie con la base de datos y los modelos proporcionados
        await init_beanie(
            database=self.client[self.database_name], document_models=self.models
        )

    async def close(self):
        # Cierra el cliente de Mongo
        self.client.close()
