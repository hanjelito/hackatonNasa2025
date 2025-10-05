<template>
  <div class="search-view">
    <NavHeader />

    <div class="main-layout">
      <div class="search-container" :class="{ 'with-sidebar': showAdvancedFilters }">
        <div class="search-content">
          <div class="search-input-row">
            <SearchInput
              v-model="searchQuery"
              placeholder="Search NASA data..."
              @search="handleSearch"
            />
            <button @click="toggleAdvancedFilters" class="filter-toggle-btn" :class="{ active: showAdvancedFilters }">
              <FunnelIcon class="w-5 h-5" />
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

          <div v-if="selectedArticleIds.length > 0" class="selected-info">
            <p>
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
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import NavHeader from '../components/NavHeader.vue'
import SearchInput from '../components/SearchInput.vue'
import SearchButton from '../components/SearchButton.vue'
import ArticleList from '../components/ArticleList.vue'
import ActiveFilters from '../components/ActiveFilters.vue'
import FilterPanel from '../components/FilterPanel.vue'
import SelectedFilterTags from '../components/SelectedFilterTags.vue'
import FunnelIcon from '../components/icons/FunnelIcon.vue'
import { searchArticles } from '../services/articleService'
import type { Article, SearchFilters } from '../types/article'
import mockData from '../data/mockArticleReal.json'
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
  const years = mockData.papers
    .filter((a: any) => a.publication_date)
    .map((a: any) => new Date(a.publication_date).getFullYear())
  return [...new Set(years)].sort((a: number, b: number) => b - a)
})

const availableOrganisms = computed(() => {
  const organisms = mockData.papers
    .filter((a: any) => a.primary_organisms_studied && a.primary_organisms_studied.length > 0)
    .flatMap((a: any) => a.primary_organisms_studied)
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
  const filterArray: { name: string; values: (string | number)[] }[] = []

  // Iterate through all filter properties
  Object.keys(searchFilters).forEach(key => {
    if (key !== 'query') {
      const values = searchFilters[key as keyof SearchFilters]
      if (Array.isArray(values) && values.length > 0) {
        filterArray.push({ name: key, values })
      }
    }
  })

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
  console.log('Filter by year:', year)
  console.log('Current filters:', activeFilters.value)
  handleSearch({
    ...activeFilters.value,
    query: searchQuery.value.trim() || undefined,
    year
  })
}

const handleFilterOrganism = (organism: string) => {
  console.log('Filter by organism:', organism)
  console.log('Current filters:', activeFilters.value)
  handleSearch({
    ...activeFilters.value,
    query: searchQuery.value.trim() || undefined,
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
  // Update filters and trigger search with current query
  handleSearch({
    ...filters,
    query: searchQuery.value.trim() || undefined
  })
}

const handleRemoveFilterTag = (filterName: string, value: string | number) => {
  const currentFilters = activeFilters.value
  const filterArray = currentFilters[filterName as keyof SearchFilters] as (string | number)[] | undefined

  if (filterArray && Array.isArray(filterArray)) {
    const updatedArray = filterArray.filter(v => v !== value)
    handleSearch({
      ...currentFilters,
      [filterName]: updatedArray.length > 0 ? updatedArray : undefined
    })
  }
}
</script>

<style scoped>
.search-view {
  min-height: 100vh;
  background-color: #000000;
}

.main-layout {
  display: flex;
  min-height: calc(100vh - 80px);
}

.search-container {
  flex: 1;
  padding: 2rem;
  transition: margin-right 0.3s ease;
}

.search-container.with-sidebar {
  margin-right: 360px;
}

.search-content {
  max-width: 1400px;
  margin: 0 auto;
  background-color: #ffffff;
  border-radius: 12px;
  padding: 2.5rem;
  box-shadow: 0 4px 24px rgba(0, 0, 0, 0.5);
}

.search-input-row {
  display: flex;
  gap: 0.75rem;
  align-items: flex-end;
  margin-bottom: 1.5rem;
}

.search-input-row > :first-child {
  flex: 1;
}

.filter-toggle-btn {
  padding: 0.75rem 1rem;
  background-color: #f5f5f5;
  border: 2px solid #e0e0e0;
  border-radius: 0.5rem;
  cursor: pointer;
  transition: all 0.2s;
  color: #58585b;
  display: flex;
  align-items: center;
  justify-content: center;
  height: 3.25rem;
  width: 3.25rem;
  flex-shrink: 0;
}

.filter-toggle-btn:hover {
  border-color: #0b3d91;
  color: #0b3d91;
  background-color: #e8f4ff;
}

.filter-toggle-btn.active {
  border-color: #0b3d91;
  background-color: #0b3d91;
  color: white;
}

.selected-info {
  margin-top: 1.5rem;
  padding: 1rem;
  background-color: #e8f4ff;
  border: 1px solid #0b3d91;
  border-radius: 6px;
  color: #0056b3;
  font-size: 0.9rem;
  font-weight: 500;
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

@media (max-width: 1024px) {
  .search-container {
    padding: 1.5rem;
  }

  .search-container.with-sidebar {
    margin-right: 0;
  }
}

@media (max-width: 768px) {
  .search-container {
    padding: 1rem;
  }

  .search-content {
    padding: 1.5rem;
  }

  .filters-row {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 640px) {
  .search-input-row {
    flex-wrap: wrap;
  }

  .search-content {
    padding: 1rem;
  }
}
</style>
