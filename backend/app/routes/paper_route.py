from fastapi import APIRouter

from app.dto.filter_value import FilterValue
from app.dto.search_papers_request import SearchPapersRequest
from app.models.paper import Paper
from app.services.paper_service import search_papers_similars, obtain_paper_filters_values

paper_router = APIRouter(
    prefix="/paper",
    tags=["Papers"],
)

@paper_router.post("/search", response_model=list[Paper])
async def search_papers(search_filters: SearchPapersRequest):
    return await search_papers_similars(search_filters)

@paper_router.get("/search/filters", response_model=list[FilterValue])
async def obtain_filters_values():
    return obtain_paper_filters_values()