from typing import Type
from pymongo import AsyncMongoClient
from beanie import init_beanie, Document
from app.models.paper import Paper


class MongoDbClient:
    async def __init__(self, url: str, database_name: str = "hackaton_nasa_db"):
        self.models: list[Type[Document]] = [Paper]
        self.client = AsyncMongoClient(url)
        self.database_name = database_name

    async def init(self):
        await init_beanie(
            database=self.client[self.database_name], document_models=self.models
        )

    async def close(self):
        await self.client.close()
