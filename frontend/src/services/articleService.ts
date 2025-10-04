import type { Article, SearchResponse, SearchFilters } from '../types/article'
import mockData from '../data/mockArticles.json'

export const searchArticles = async (filters: SearchFilters): Promise<SearchResponse> => {
  // Log del query para el API
  console.log('🔍 API Query:', JSON.stringify(filters, null, 2))

  // Simular un delay de red
  await new Promise(resolve => setTimeout(resolve, 500))

  let filteredArticles = mockData.articles as Article[]

  // Filtrar por query de búsqueda
  if (filters.query && filters.query.trim()) {
    filteredArticles = filteredArticles.filter((article: Article) =>
      article.title.toLowerCase().includes(filters.query!.toLowerCase()) ||
      article.description.toLowerCase().includes(filters.query!.toLowerCase())
    )
  }

  // Filtrar por año
  if (filters.year) {
    filteredArticles = filteredArticles.filter((article: Article) =>
      article.year === filters.year
    )
  }

  // Filtrar por organismo
  if (filters.organism) {
    filteredArticles = filteredArticles.filter((article: Article) =>
      article.organism.toLowerCase() === filters.organism!.toLowerCase()
    )
  }

  return {
    query: filters.query || '',
    total: filteredArticles.length,
    articles: filteredArticles
  }
}
