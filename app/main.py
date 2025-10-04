from fastapi import FastAPI
from routes.paper_route import paper_router

app = FastAPI()

app.include_router(paper_router)
# app.include_router(event_router)
# app.include_router(ticket_route)
