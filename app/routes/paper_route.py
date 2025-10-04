from fastapi import APIRouter
from app.services.paper_service import search_papers_similars, obtain_paper_filters

paper_router = APIRouter(
    prefix="/paper",
    tags=["Papers"],
)

@paper_router.get("/search", response_model=list[str])
async def search_papers(query: str):
    return await search_papers_similars(query)

@paper_router.get("/search/filters", response_model=list[str])
async def obtain_filters_values():
    return await obtain_paper_filters_values()