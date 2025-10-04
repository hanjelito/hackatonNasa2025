export interface Article {
  id: string
  title: string
  description: string
  date: string
  source: string
  year: number
  organism: string
  authors: string[]
  imageUrl?: string
}

export interface SearchResponse {
  query: string
  total: number
  articles: Article[]
}

export interface SearchFilters {
  query?: string
  year?: number
  organism?: string
}

export interface SelectedArticle {
  articleId: string
  selected: boolean
}
