from fastapi import APIRouter

from app.dto.filter_value import FilterValue
from app.dto.search_papers_request import SearchPapersRequest
from app.models.paper import Paper
from app.services.paper_service import search_papers_similars, obtain_paper_filters_values, obtain_paper_detail

paper_router = APIRouter(
    prefix="/paper",
    tags=["Papers"],
)

@paper_router.post("/search", response_model=list[Paper])
async def search_papers(search_filters: SearchPapersRequest):
    papers = await search_papers_similars(search_filters)
    for paper in papers:
        if hasattr(paper, "full_text"):
            delattr(paper, "full_text")
    return papers

@paper_router.get("/search/filters", response_model=list[FilterValue])
async def obtain_filters_values():
    return obtain_paper_filters_values()

@paper_router.get("/{id}", response_model=Paper)
async def obtain_detail(id: str):
    paper = await obtain_paper_detail(id)
    if hasattr(paper, "full_text"):
        delattr(paper, "full_text")
    return paper