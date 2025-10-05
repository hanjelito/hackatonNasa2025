<template>
  <div class="article-list">
    <div v-if="loading" class="loading">
      <p>Loading articles...</p>
    </div>

    <div v-else-if="articles.length === 0" class="no-results">
      <p>No articles found. Try a different search term.</p>
    </div>

    <div v-else>
      <div class="list-header">
        <h2>{{ total }} article{{ total !== 1 ? 's' : '' }} found</h2>
        <div v-if="selectedCount > 0" class="selected-info">
          {{ selectedCount }} selected
        </div>
      </div>

      <div class="articles-container">
        <ArticleCard
          v-for="article in articles"
          :key="article.id"
          :article="article"
          :selected="isSelected(article._id)"
          @toggle="handleToggle"
          @filter-year="handleFilterYear"
          @filter-organism="handleFilterOrganism"
        />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import type { Article } from '../types/article'
import ArticleCard from './ArticleCard.vue'

const props = defineProps<{
  articles: Article[]
  selectedIds: string[]
  loading?: boolean
  total?: number
}>()

const emit = defineEmits<{
  'toggle-selection': [id: string]
  'filter-year': [year: number]
  'filter-organism': [organism: string]
}>()

const selectedCount = computed(() => props.selectedIds.length)

const isSelected = (id?: string) => {
  if (!id) return false
  return props.selectedIds.includes(id)
}

const handleToggle = (id: string) => {
  emit('toggle-selection', id)
}

const handleFilterYear = (year: number) => {
  emit('filter-year', year)
}

const handleFilterOrganism = (organism: string) => {
  emit('filter-organism', organism)
}
</script>

<style scoped>
@import '../assets/css/article-list.css';
</style>
