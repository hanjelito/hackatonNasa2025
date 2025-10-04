from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.config.mongodb_client import MongoDbClient
from app.routes.paper_route import paper_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    database = MongoDbClient()
    await database.init()
    yield
    await database.close()


app = FastAPI(lifespan=lifespan)

def create_app() -> FastAPI:
    fast_api = FastAPI(lifespan=lifespan)

    return fast_api

app = create_app()


app.include_router(paper_router)
# app.include_router(event_router)
# app.include_router(ticket_route)
