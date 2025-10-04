<template>
  <div class="filter-panel" :class="{ 'is-open': isOpen }">
    <div class="panel-header">
      <h3>Advanced Filters</h3>
      <button @click="$emit('close')" class="close-btn">×</button>
    </div>

    <div class="panel-content">
      <AutocompleteInput
        id="year-filter"
        label="Year"
        placeholder="Type at least 3 characters..."
        :options="yearOptions"
        :model-value="filters.year"
        :min-chars="3"
        @update:model-value="handleYearChange"
      />

      <AutocompleteInput
        id="organism-filter"
        label="Organization"
        placeholder="Type at least 2 characters..."
        :options="organismOptions"
        :model-value="filters.organism"
        :min-chars="1"
        @update:model-value="handleOrganismChange"
      />

      <div class="panel-actions">
        <button @click="handleApply" class="apply-btn">
          Apply Filters
        </button>
        <button @click="handleClear" class="clear-btn">
          Clear
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'
import AutocompleteInput from './AutocompleteInput.vue'
import type { SearchFilters } from '../types/article'

const props = defineProps<{
  isOpen: boolean
  filters: SearchFilters
  yearOptions: number[]
  organismOptions: string[]
}>()

const emit = defineEmits<{
  'close': []
  'apply': [filters: SearchFilters]
}>()

const localYear = ref<number | undefined>(props.filters.year)
const localOrganism = ref<string | undefined>(props.filters.organism)

watch(() => props.filters, (newFilters) => {
  localYear.value = newFilters.year
  localOrganism.value = newFilters.organism
}, { deep: true })

const handleYearChange = (value: string | number | undefined) => {
  localYear.value = typeof value === 'string' ? parseInt(value) : value
}

const handleOrganismChange = (value: string | number | undefined) => {
  localOrganism.value = value?.toString()
}

const handleApply = () => {
  emit('apply', {
    ...props.filters,
    year: localYear.value,
    organism: localOrganism.value
  })
  emit('close')
}

const handleClear = () => {
  localYear.value = undefined
  localOrganism.value = undefined
}
</script>

<style scoped>
@import '../assets/css/filter-panel.css';
</style>
