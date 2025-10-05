from typing import List
from fastapi import HTTPException
from app.dto.search_papers_request import SearchPapersRequest
from app.dto.filter_value import FilterValue
from app.models.paper import Paper
from app.models.enums.study_type import StudyType
from app.models.enums.experimental_platform import ExperimentalPlatform
from app.models.enums.stressor import Stressor
from app.models.enums.organism import Organism
from app.models.enums.space_agency import SpaceAgency


async def search_papers_similars(search_filters: SearchPapersRequest) -> List[Paper]:
    """
    Busca papers utilizando MongoDB Atlas Search con compound operator.
    Combina búsqueda de texto en todos los campos con filtros específicos.
    """

    # Construir la cláusula 'must' para la búsqueda de texto
    must_clauses = []

    # Agregar búsqueda de texto si hay query
    if search_filters.query and search_filters.query.strip():
        must_clauses.append({
            "text": {
                "query": search_filters.query,
                "path": {
                    "wildcard": "*"  # Busca en todos los campos
                }
            }
        })

    # Construir la cláusula 'filter' para los filtros específicos
    filter_clauses = []

    # Procesar cada filtro
    for filter_item in search_filters.filters:
        if filter_item.values and len(filter_item.values) > 0:
            # El nombre del filtro coincide con el nombre del campo en el modelo
            field_name = filter_item.name

            # Usar el operador 'in' para manejar uno o más valores
            # TODO: Crear índices específicos para estos campos chat gpt (Documentación MongoDB compound)
            filter_clauses.append({
                "in": {
                    "path": field_name,
                    "value": filter_item.values
                }
            })

    # Si no hay ni query ni filtros, usar find() simple
    if not must_clauses and not filter_clauses:
        try:
            return await Paper.find_all().limit(search_filters.limit).to_list()
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error searching papers: {str(e)}")

    # Construir la pipeline de agregación con $search
    search_stage = {
        "$search": {
            "index": "search_index",
            "compound": {}
        }
    }

    if must_clauses:
        search_stage["$search"]["compound"]["must"] = must_clauses

    if filter_clauses:
        search_stage["$search"]["compound"]["filter"] = filter_clauses

    pipeline = [
        search_stage,
        {"$limit": search_filters.limit},
        {
            "$addFields": {
                "search_score": {"$meta": "searchScore"}
            }
        }
    ]

    # Ejecutar la búsqueda y retornar resultados
    try:
        results = await Paper.aggregate(pipeline).to_list()
        return [Paper.model_validate(doc) for doc in results]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error searching papers: {str(e)}")


def obtain_paper_filters_values():
    filters: list[FilterValue] = [
        FilterValue(
            name="Study Type",
            values=[enum_value.value for enum_value in StudyType]
        ),
        FilterValue(
            name="Experimental Platform",
            values=[enum_value.value for enum_value in ExperimentalPlatform]
        ),
        FilterValue(
            name="Space Environment Stressors",
            values=[enum_value.value for enum_value in Stressor]
        ),
        FilterValue(
            name="Primary Organisms Studied",
            values=[enum_value.value for enum_value in Organism]
        ),
        FilterValue(
            name="Space Agency Involvement",
            values=[enum_value.value for enum_value in SpaceAgency]
        ),
    ]

    return filters