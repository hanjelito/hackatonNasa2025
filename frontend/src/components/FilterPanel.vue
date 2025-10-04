<template>
  <div class="filter-panel" :class="{ 'is-open': isOpen }">
    <div class="panel-header">
      <h3>Advanced Filters</h3>
      <button @click="$emit('close')" class="close-btn">×</button>
    </div>

    <div class="panel-content">
      <div v-if="loading" class="loading-message">Loading filters...</div>

      <div v-else-if="error" class="error-message">{{ error }}</div>

      <template v-else>
        <MultiSelectFilter
          v-for="filter in dynamicFilters"
          :key="filter.name"
          :id="`${filter.name}-filter`"
          :label="filter.name"
          :options="filter.values"
          :model-value="localFilters[filter.name] || []"
          @update:model-value="handleFilterChange(filter.name, $event)"
        />
      </template>

      <div class="panel-actions">
        <button @click="handleClear" class="clear-btn">
          Clear All Filters
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch, onMounted, reactive } from 'vue'
import MultiSelectFilter from './MultiSelectFilter.vue'
import type { SearchFilters, FilterOption } from '../types/article'

const props = defineProps<{
  isOpen: boolean
  filters: SearchFilters
}>()

const emit = defineEmits<{
  'close': []
  'update:filters': [filters: SearchFilters]
}>()

const dynamicFilters = ref<FilterOption[]>([])
const loading = ref(false)
const error = ref<string | null>(null)
const localFilters = reactive<Record<string, (string | number)[]>>({})

const loadFilters = async () => {
  loading.value = true
  error.value = null

  try {
    const response = await fetch('/api/paper/search/filters')
    if (!response.ok) {
      throw new Error('Failed to load filters')
    }
    const data = await response.json()
    dynamicFilters.value = data

    // Initialize local filters
    data.forEach((filter: FilterOption) => {
      localFilters[filter.name] = props.filters[filter.name as keyof SearchFilters] as (string | number)[] || []
    })
  } catch (err) {
    error.value = 'Error loading filters. Please try again.'
    console.error('Error loading filters:', err)
  } finally {
    loading.value = false
  }
}

watch(() => props.filters, (newFilters: SearchFilters) => {
  dynamicFilters.value.forEach((filter: FilterOption) => {
    localFilters[filter.name] = newFilters[filter.name as keyof SearchFilters] as (string | number)[] || []
  })
}, { deep: true })

const handleFilterChange = (filterName: string, values: (string | number)[]) => {
  localFilters[filterName] = values

  // Emit updated filters immediately
  emit('update:filters', {
    ...props.filters,
    ...localFilters
  })
}

const handleClear = () => {
  dynamicFilters.value.forEach((filter: FilterOption) => {
    localFilters[filter.name] = []
  })

  // Emit cleared filters
  emit('update:filters', {
    ...props.filters,
    organisms: undefined,
    years: undefined,
    sources: undefined,
    article_types: undefined
  })
}

onMounted(() => {
  loadFilters()
})
</script>

<style scoped>
@import '../assets/css/filter-panel.css';
</style>
