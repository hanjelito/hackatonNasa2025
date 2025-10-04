from fastapi import FastAPI
from app.routes.paper_route import paper_router


def create_app() -> FastAPI:
    fast_api = FastAPI()
    fast_api.include_router(paper_router)
    return fast_api

app = FastAPI()

app.include_router(paper_router)
# app.include_router(event_router)
# app.include_router(ticket_route)