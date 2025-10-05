import type { Article, SearchResponse, SearchFilters } from '../types/article'
import mockData from '../data/mockArticleReal.json'

export const searchArticles = async (filters: SearchFilters): Promise<SearchResponse> => {
  // Simular un delay de red
  await new Promise(resolve => setTimeout(resolve, 500))

  let filteredArticles = mockData.papers as Article[]

  // Filtrar por query de búsqueda
  if (filters.query && filters.query.trim()) {
    filteredArticles = filteredArticles.filter((article: Article) =>
      article.title.toLowerCase().includes(filters.query!.toLowerCase()) ||
      (article.abstract || '').toLowerCase().includes(filters.query!.toLowerCase())
    )
  }

  // Filtrar por año (usando publication_date)
  if (filters.year) {
    filteredArticles = filteredArticles.filter((article: Article) => {
      if (article.publication_date) {
        const year = new Date(article.publication_date).getFullYear()
        return year === filters.year
      }
      return false
    })
  }

  // Filtrar por organismo
  if (filters.organism) {
    filteredArticles = filteredArticles.filter((article: Article) =>
      article.primary_organisms_studied?.some(org =>
        org.toLowerCase().includes(filters.organism!.toLowerCase())
      )
    )
  }

  return {
    query: filters.query || '',
    total: filteredArticles.length,
    articles: filteredArticles
  }
}
