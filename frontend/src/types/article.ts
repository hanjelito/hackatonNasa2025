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
  organisms?: string[]
  years?: number[]
  sources?: string[]
}

export interface FilterOption {
  name: string
  values: (string | number)[]
}

export interface FiltersConfig {
  filters: FilterOption[]
}

export interface SelectedArticle {
  articleId: string
  selected: boolean
}
