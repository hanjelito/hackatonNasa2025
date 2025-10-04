import asyncio
from app.dto.search_papers_request import SearchPapersRequest
from app.dto.filter_value import FilterValue
from app.models.paper import Paper

def search_papers_similars(search_filters: SearchPapersRequest):

    # Aquí iría la lógica para buscar papers en Atlas search
    # Por ahora, devolvemos una lista de ejemplo
    example_papers = [
        "Paper 1: Análisis de Algoritmos",
        "Paper 2: Introducción a la Inteligencia Artificial",
        "Paper 3: Redes Neuronales y Deep Learning",
        "Paper 4: Procesamiento de Lenguaje Natural",
        "Paper 5: Visión por Computadora"
    ]

    # Filtrar los papers que contienen la consulta
    filtered_papers = [paper for paper in example_papers if query.lower() in paper.lower()]

    return filtered_papers


async def obtain_paper_filters_values():
    await asyncio.sleep(0)
    paper = Paper(prueba="prueba")
    await paper.insert()
    # Respuesta de ejemplo con la misma forma que el DTO FilterValue
    example_filters: list[FilterValue] = [
        FilterValue(
            name="organisms",
            values=[
                "Human",
                "Mouse",
                "Rat",
                "Zebrafish",
                "Fruit fly",
                "Nematode",
                "Yeast",
            ],
        ),
        FilterValue(
            name="article_types",
            values=[
                "Review",
                "Research Article",
                "Short Communication",
                "Case Report",
            ],
        ),
    ]

    return example_filters