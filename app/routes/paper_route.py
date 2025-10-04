from fastapi import APIRouter

from dto.filter_value import FilterValue
from dto.search_papers_request import SearchPapersRequest
from services.paper_service import search_papers_similars, obtain_paper_filters_values

paper_router = APIRouter(
    prefix="/paper",
    tags=["Papers"],
)

@paper_router.post("/search", response_model=list[str])
async def search_papers(search_filters: SearchPapersRequest):
    return await search_papers_similars(search_filters)

@paper_router.get("/search/filters", response_model=list[FilterValue])
async def obtain_filters_values():
    return await obtain_paper_filters_values()