from dto.search_papers_request import SearchPapersRequest


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

def obtain_paper_filters_values():
    # Aquí iría la lógica para obtener los filtros de papers desde la base de datos
    # Por ahora, devolvemos una lista de ejemplo
    example_filters = [
        "Algoritmos",
        "Inteligencia Artificial",
        "Redes Neuronales",
        "Procesamiento de Lenguaje Natural",
        "Visión por Computadora"
    ]

    return example_filters