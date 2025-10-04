<template>
  <div class="search-view">
    <NavHeader />

    <div class="search-container">
      <div class="search-content">
        <div class="search-input-row">
          <SearchInput
            v-model="searchQuery"
            placeholder="Search NASA data..."
            @search="handleSearch"
          />
          <button @click="toggleAdvancedFilters" class="filter-toggle-btn" :class="{ active: showAdvancedFilters }">
            <AdjustmentsHorizontalIcon class="w-5 h-5" />
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
import AdjustmentsHorizontalIcon from '../components/icons/AdjustmentsHorizontalIcon.vue'
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
.search-view {
  min-height: 100vh;
  background-color: #000000;
}

.search-container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 2rem;
}

.search-content {
  background-color: #1a1a1a;
  border-radius: 8px;
  padding: 2rem;
  border: 1px solid #2a2a2a;
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
  padding: 0.5rem;
  background-color: #2a2a2a;
  border: 2px solid #2a2a2a;
  border-radius: 0.5rem;
  cursor: pointer;
  transition: all 0.2s;
  color: #959599;
  display: flex;
  align-items: center;
  justify-content: center;
  height: 2.75rem;
  width: 2.75rem;
  flex-shrink: 0;
}

.filter-toggle-btn:hover {
  border-color: #288bff;
  color: #288bff;
  background-color: rgba(40, 139, 255, 0.1);
}

.filter-toggle-btn.active {
  border-color: #288bff;
  background-color: #288bff;
  color: white;
}

.selected-info {
  margin-top: 1.5rem;
  padding: 1rem;
  background-color: rgba(40, 139, 255, 0.1);
  border: 1px solid #288bff;
  border-radius: 6px;
  color: #288bff;
  font-size: 0.9rem;
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
