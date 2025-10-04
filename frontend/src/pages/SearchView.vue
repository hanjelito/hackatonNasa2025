<template>
  <div class="min-h-screen bg-gray-100 py-8 px-4">
    <div class="max-w-4xl mx-auto">
      <h1 class="text-4xl font-bold text-center mb-8 text-gray-800">NASA Challenge 2025</h1>

      <div class="bg-white rounded-lg shadow-md p-6">
        <div class="search-input-row">
          <SearchInput
            v-model="searchQuery"
            placeholder="Search NASA data..."
            @search="handleSearch"
          />
          <button @click="toggleFilters" class="filter-toggle-btn" :class="{ active: showFilters }">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              width="20"
              height="20"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="2"
              stroke-linecap="round"
              stroke-linejoin="round"
            >
              <polygon points="22 3 2 3 10 12.46 10 19 14 21 14 12.46 22 3"></polygon>
            </svg>
          </button>
        </div>

        <div v-if="showFilters" class="filters-row">
          <AutocompleteInput
            id="year-filter-main"
            label="Year"
            placeholder="Type year..."
            :options="availableYears"
            :model-value="activeFilters.year"
            :min-chars="3"
            @update:model-value="handleYearFilterChange"
          />
          <AutocompleteInput
            id="organism-filter-main"
            label="Organization"
            placeholder="Type organization..."
            :options="availableOrganisms"
            :model-value="activeFilters.organism"
            :min-chars="1"
            @update:model-value="handleOrganismFilterChange"
          />
        </div>

        <SearchButton @click="handleSearch" />

        <ActiveFilters
          :filters="activeFilters"
          @remove-year="handleRemoveYear"
          @remove-organism="handleRemoveOrganism"
          @remove-query="handleRemoveQuery"
          @clear-all="handleClearAll"
        />

        <ArticleList
          :articles="articles"
          :selected-ids="selectedArticleIds"
          :loading="loading"
          :total="totalResults"
          @toggle-selection="handleToggleSelection"
          @filter-year="handleFilterYear"
          @filter-organism="handleFilterOrganism"
        />

        <div v-if="selectedArticleIds.length > 0" class="mt-6 p-4 bg-blue-50 rounded-lg">
          <p class="text-sm text-blue-800">
            You have selected {{ selectedArticleIds.length }} article{{ selectedArticleIds.length !== 1 ? 's' : '' }}
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import SearchInput from '../components/SearchInput.vue'
import SearchButton from '../components/SearchButton.vue'
import AutocompleteInput from '../components/AutocompleteInput.vue'
import ArticleList from '../components/ArticleList.vue'
import ActiveFilters from '../components/ActiveFilters.vue'
import { searchArticles } from '../services/articleService'
import type { Article, SearchFilters } from '../types/article'
import mockData from '../data/mockArticles.json'
import { useSearchState } from '../composables/useSearchState'

// Usar el estado compartido
const {
  searchQuery,
  articles,
  selectedArticleIds,
  totalResults,
  activeFilters,
  setSearchQuery,
  setArticles,
  setSelectedArticleIds,
  setTotalResults,
  setActiveFilters,
  clearSearchState
} = useSearchState()

const loading = ref(false)
const showFilters = ref(false)

// Get unique years and organisms from mock data
const availableYears = computed(() => {
  const years = mockData.articles.map((a: Article) => a.year)
  return [...new Set(years)].sort((a, b) => b - a)
})

const availableOrganisms = computed(() => {
  const organisms = mockData.articles.map((a: Article) => a.organism)
  return [...new Set(organisms)].sort()
})

const handleSearch = async (filters?: SearchFilters) => {
  loading.value = true
  setSelectedArticleIds([])

  // Si no se pasan filtros, mantener los filtros activos y solo actualizar el query
  const searchFilters: SearchFilters = filters || {
    ...activeFilters.value,
    query: searchQuery.value.trim() || undefined
  }

  setActiveFilters(searchFilters)

  try {
    const response = await searchArticles(searchFilters)
    setArticles(response.articles)
    setTotalResults(response.total)
  } catch (error) {
    console.error('Error searching articles:', error)
    setArticles([])
    setTotalResults(0)
  } finally {
    loading.value = false
  }
}

const handleToggleSelection = (articleId: string) => {
  const index = selectedArticleIds.value.indexOf(articleId)
  if (index > -1) {
    selectedArticleIds.value.splice(index, 1)
  } else {
    selectedArticleIds.value.push(articleId)
  }
}

const handleFilterYear = (year: number) => {
  handleSearch({
    ...activeFilters.value,
    year
  })
}

const handleFilterOrganism = (organism: string) => {
  handleSearch({
    ...activeFilters.value,
    organism
  })
}

const handleRemoveYear = () => {
  const { year, ...rest } = activeFilters.value
  handleSearch(rest)
}

const handleRemoveOrganism = () => {
  const { organism, ...rest } = activeFilters.value
  handleSearch(rest)
}

const handleRemoveQuery = () => {
  setSearchQuery('')
  const { query, ...rest } = activeFilters.value
  handleSearch(rest)
}

const handleClearAll = () => {
  clearSearchState()
}

const handleYearFilterChange = (value: string | number | undefined) => {
  const year = typeof value === 'string' ? parseInt(value) : value
  handleSearch({
    ...activeFilters.value,
    year
  })
}

const handleOrganismFilterChange = (value: string | number | undefined) => {
  handleSearch({
    ...activeFilters.value,
    organism: value?.toString()
  })
}

const toggleFilters = () => {
  showFilters.value = !showFilters.value
}
</script>

<style scoped>
.search-input-row {
  display: flex;
  gap: 0.5rem;
  align-items: flex-end;
  margin-bottom: 1rem;
}

.search-input-row > :first-child {
  flex: 1;
}

.filter-toggle-btn {
  padding: 0.5rem;
  background-color: white;
  border: 2px solid #d1d5db;
  border-radius: 0.5rem;
  cursor: pointer;
  transition: all 0.2s;
  color: #6b7280;
  display: flex;
  align-items: center;
  justify-content: center;
  height: 2.5rem;
  width: 2.5rem;
  flex-shrink: 0;
}

.filter-toggle-btn:hover {
  border-color: #2563eb;
  color: #2563eb;
  background-color: #eff6ff;
}

.filter-toggle-btn.active {
  border-color: #2563eb;
  background-color: #2563eb;
  color: white;
}

.filters-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
  margin-bottom: 1rem;
  animation: slideDown 0.2s ease-out;
}

@keyframes slideDown {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@media (max-width: 640px) {
  .filters-row {
    grid-template-columns: 1fr;
  }

  .search-input-row {
    flex-wrap: wrap;
  }
}
</style>
