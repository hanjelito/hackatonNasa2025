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

  // Process article_types
  if (props.filters.article_types && props.filters.article_types.length > 0) {
    props.filters.article_types.forEach(type => {
      tags.push({
        key: `article_types-${type}`,
        label: 'Article Type',
        value: type,
        filterName: 'article_types'
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
  gap: 0.75rem;
  margin-top: 1rem;
  margin-bottom: 1rem;
}

.tag {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  background-color: rgba(40, 139, 255, 0.15);
  color: #288bff;
  border: 1px solid rgba(40, 139, 255, 0.3);
  border-radius: 6px;
  font-size: 0.875rem;
  font-weight: 600;
}

.remove-tag {
  background: none;
  border: none;
  color: #288bff;
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
  background-color: rgba(40, 139, 255, 0.3);
}
</style>
