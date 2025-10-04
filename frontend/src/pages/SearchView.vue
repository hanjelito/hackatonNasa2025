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
          <button @click="toggleAdvancedFilters" class="filter-toggle-btn" :class="{ active: showAdvancedFilters }">
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
              <line x1="4" y1="21" x2="4" y2="14"></line>
              <line x1="4" y1="10" x2="4" y2="3"></line>
              <line x1="12" y1="21" x2="12" y2="12"></line>
              <line x1="12" y1="8" x2="12" y2="3"></line>
              <line x1="20" y1="21" x2="20" y2="16"></line>
              <line x1="20" y1="12" x2="20" y2="3"></line>
              <line x1="1" y1="14" x2="7" y2="14"></line>
              <line x1="9" y1="8" x2="15" y2="8"></line>
              <line x1="17" y1="16" x2="23" y2="16"></line>
            </svg>
          </button>
        </div>

        <SearchButton @click="handleSearch" />

        <SelectedFilterTags
          :filters="activeFilters"
          @remove="handleRemoveFilterTag"
        />

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

    <FilterPanel
      :is-open="showAdvancedFilters"
      :filters="activeFilters"
      @close="showAdvancedFilters = false"
      @update:filters="handleUpdateFilters"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import SearchInput from '../components/SearchInput.vue'
import SearchButton from '../components/SearchButton.vue'
import ArticleList from '../components/ArticleList.vue'
import ActiveFilters from '../components/ActiveFilters.vue'
import FilterPanel from '../components/FilterPanel.vue'
import SelectedFilterTags from '../components/SelectedFilterTags.vue'
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
const showAdvancedFilters = ref(false)

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

  // Build filters array in the required format for console log
  const filterArray = []
  if (searchFilters.organisms && searchFilters.organisms.length > 0) {
    filterArray.push({ name: 'organisms', values: searchFilters.organisms })
  }
  if (searchFilters.years && searchFilters.years.length > 0) {
    filterArray.push({ name: 'years', values: searchFilters.years })
  }
  if (searchFilters.sources && searchFilters.sources.length > 0) {
    filterArray.push({ name: 'sources', values: searchFilters.sources })
  }

  const payload = {
    filters: filterArray,
    query: searchFilters.query || ''
  }

  console.log('Filters to send (POST):', JSON.stringify(payload, null, 2))

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

const toggleAdvancedFilters = () => {
  showAdvancedFilters.value = !showAdvancedFilters.value
}

const handleUpdateFilters = (filters: SearchFilters) => {
  // Just update the active filters without searching
  setActiveFilters(filters)
}

const handleRemoveFilterTag = (filterName: string, value: string | number) => {
  const currentFilters = activeFilters.value
  const filterArray = currentFilters[filterName as keyof SearchFilters] as (string | number)[] | undefined

  if (filterArray && Array.isArray(filterArray)) {
    const updatedArray = filterArray.filter(v => v !== value)
    setActiveFilters({
      ...currentFilters,
      [filterName]: updatedArray.length > 0 ? updatedArray : undefined
    })
  }
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
