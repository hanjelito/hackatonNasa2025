from typing import Type
from pymongo import AsyncMongoClient
from beanie import init_beanie, Document
from app.models.paper import Paper
from app.config.settings import settings


class MongoDbClient:
    def __init__(self, database_name: str = "hackaton_nasa_db"):
        self.models: list[Type[Document]] = [Paper]
        self.client = AsyncMongoClient(settings.MONGODB_URL)
        self.database_name = database_name

    async def init(self):
        try:
            await init_beanie(
                database=self.client[self.database_name], document_models=self.models
            )
        except Exception as e:
            raise ValueError(f"Error initializing database: {e}")

    async def close(self):
        try:
            await self.client.close()
        except Exception as e:
            raise ValueError(f"Error closing database connection: {e}")