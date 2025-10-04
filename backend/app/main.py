from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.routes.paper_route import paper_router
from app.config.mongodb_client import MongoDbClient

database = MongoDbClient()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Inicializar la conexión a la base de datos
    await database.init()
    yield
    # Shutdown: Cerrar la conexión a la base de datos
    await database.close()

app = FastAPI(lifespan=lifespan)

app.include_router(paper_router)
# app.include_router(event_router)
# app.include_router(ticket_route)