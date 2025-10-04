<template>
  <div v-if="hasSelectedFilters" class="selected-filter-tags">
    <span
      v-for="tag in filterTags"
      :key="tag.key"
      class="tag"
    >
      {{ tag.label }}: {{ tag.value }}
      <button @click="removeTag(tag)" class="remove-tag">×</button>
    </span>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import type { SearchFilters } from '../types/article'

const props = defineProps<{
  filters: SearchFilters
}>()

const emit = defineEmits<{
  'remove': [filterName: string, value: string | number]
}>()

interface FilterTag {
  key: string
  label: string
  value: string | number
  filterName: string
}

const filterTags = computed(() => {
  const tags: FilterTag[] = []

  // Process organisms
  if (props.filters.organisms && props.filters.organisms.length > 0) {
    props.filters.organisms.forEach(org => {
      tags.push({
        key: `organisms-${org}`,
        label: 'Organization',
        value: org,
        filterName: 'organisms'
      })
    })
  }

  // Process years
  if (props.filters.years && props.filters.years.length > 0) {
    props.filters.years.forEach(year => {
      tags.push({
        key: `years-${year}`,
        label: 'Year',
        value: year,
        filterName: 'years'
      })
    })
  }

  // Process sources
  if (props.filters.sources && props.filters.sources.length > 0) {
    props.filters.sources.forEach(source => {
      tags.push({
        key: `sources-${source}`,
        label: 'Source',
        value: source,
        filterName: 'sources'
      })
    })
  }

  return tags
})

const hasSelectedFilters = computed(() => filterTags.value.length > 0)

const removeTag = (tag: FilterTag) => {
  emit('remove', tag.filterName, tag.value)
}
</script>

<style scoped>
.selected-filter-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-top: 1rem;
  margin-bottom: 1rem;
}

.tag {
  display: inline-flex;
  align-items: center;
  gap: 0.25rem;
  padding: 0.375rem 0.75rem;
  background-color: #e6f0ff;
  color: #0066cc;
  border-radius: 9999px;
  font-size: 0.875rem;
  font-weight: 500;
}

.remove-tag {
  background: none;
  border: none;
  color: #0066cc;
  cursor: pointer;
  font-size: 1.25rem;
  line-height: 1;
  padding: 0;
  margin-left: 0.25rem;
  transition: color 0.2s;
}

.remove-tag:hover {
  color: #004499;
}
</style>
