from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.routes.paper_route import paper_router
from app.config.mongodb_client import MongoDbClient
from app.routes.chat_route import chat_router


database = MongoDbClient()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Inicializar la conexión a la base de datos
    await database.init()
    yield
    # Shutdown: Cerrar la conexión a la base de datos
    await database.close()

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

app.include_router(paper_router)
app.include_router(chat_router)