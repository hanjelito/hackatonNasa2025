<template>
  <div v-if="hasFilters" class="active-filters">
    <div class="filters-header">
      <h3>Active Filters:</h3>
      <button @click="$emit('clear-all')" class="clear-all-btn">
        Clear All
      </button>
    </div>
    <div class="filters-list">
      <div v-if="filters.year" class="filter-chip year">
        <span>Year: {{ filters.year }}</span>
        <button @click="$emit('remove-year')" class="remove-btn">×</button>
      </div>
      <div v-if="filters.organism" class="filter-chip organism">
        <span>Org: {{ filters.organism }}</span>
        <button @click="$emit('remove-organism')" class="remove-btn">×</button>
      </div>
      <div v-if="filters.query" class="filter-chip query">
        <span>Search: "{{ filters.query }}"</span>
        <button @click="$emit('remove-query')" class="remove-btn">×</button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import type { SearchFilters } from '../types/article'

const props = defineProps<{
  filters: SearchFilters
}>()

defineEmits<{
  'remove-year': []
  'remove-organism': []
  'remove-query': []
  'clear-all': []
}>()

const hasFilters = computed(() => {
  return !!(props.filters.year || props.filters.organism || props.filters.query)
})
</script>

<style scoped>
@import '../assets/css/active-filters.css';
</style>
