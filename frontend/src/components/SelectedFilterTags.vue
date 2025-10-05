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

const formatLabel = (filterName: string): string => {
  const labels: Record<string, string> = {
    organism: 'Organism',
    organisms: 'Organism',
    year: 'Year',
    years: 'Year',
    sources: 'Source',
    article_types: 'Article Type'
  }

  return labels[filterName] || filterName.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())
}

const filterTags = computed(() => {
  const tags: FilterTag[] = []

  // Iterate through all filter properties dynamically
  Object.entries(props.filters).forEach(([key, value]) => {
    // Skip query field and undefined/null values
    if (key === 'query' || !value) return

    // Handle array filters
    if (Array.isArray(value)) {
      value.forEach(item => {
        tags.push({
          key: `${key}-${item}`,
          label: formatLabel(key),
          value: item,
          filterName: key
        })
      })
    }
    // Handle single value filters (year, organism)
    else {
      tags.push({
        key: `${key}-${value}`,
        label: formatLabel(key),
        value: value,
        filterName: key
      })
    }
  })

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
  gap: 0.75rem;
  margin-top: 1rem;
  margin-bottom: 1rem;
}

.tag {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  background-color: rgba(11, 61, 145, 0.15);
  color: #0b3d91;
  border: 1px solid rgba(11, 61, 145, 0.3);
  border-radius: 6px;
  font-size: 0.875rem;
  font-weight: 600;
}

.remove-tag {
  background: none;
  border: none;
  color: #0b3d91;
  cursor: pointer;
  font-size: 1.25rem;
  line-height: 1;
  padding: 0;
  margin-left: 0.25rem;
  transition: all 0.2s;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 1.25rem;
  height: 1.25rem;
  border-radius: 50%;
}

.remove-tag:hover {
  background-color: rgba(11, 61, 145, 0.3);
}
</style>
