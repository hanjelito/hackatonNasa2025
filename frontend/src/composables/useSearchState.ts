import { ref } from 'vue'
import type { Article, SearchFilters } from '../types/article'

// Estado global compartido entre componentes
const searchQuery = ref('')
const articles = ref<Article[]>([])
const selectedArticleIds = ref<string[]>([])
const totalResults = ref(0)
const activeFilters = ref<SearchFilters>({})

export function useSearchState() {
  const setSearchQuery = (query: string) => {
    searchQuery.value = query
  }

  const setArticles = (newArticles: Article[]) => {
    articles.value = newArticles
  }

  const setSelectedArticleIds = (ids: string[]) => {
    selectedArticleIds.value = ids
  }

  const setTotalResults = (total: number) => {
    totalResults.value = total
  }

  const setActiveFilters = (filters: SearchFilters) => {
    activeFilters.value = filters
  }

  const clearSearchState = () => {
    searchQuery.value = ''
    articles.value = []
    selectedArticleIds.value = []
    totalResults.value = 0
    activeFilters.value = {}
  }

  return {
    // Estado
    searchQuery,
    articles,
    selectedArticleIds,
    totalResults,
    activeFilters,

    // Métodos
    setSearchQuery,
    setArticles,
    setSelectedArticleIds,
    setTotalResults,
    setActiveFilters,
    clearSearchState
  }
}
