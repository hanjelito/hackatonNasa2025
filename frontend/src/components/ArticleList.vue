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
        </div>
      </div>

      <div class="articles-container">
        <ArticleCard
          v-for="article in articles"
          :key="article.id"
          :article="article"
          :selected=false
          @toggle="() => {}"
          @filter-year="handleFilterYear"
          @filter-organism="handleFilterOrganism"
        />
      </div>
    </div>
</template>

<script setup lang="ts">
import type { Article } from '../types/article'
import ArticleCard from './ArticleCard.vue'

defineProps<{
  articles: Article[]
  selectedIds: string[]
  loading?: boolean
  total?: number
}>()

const emit = defineEmits<{
  'filter-year': [year: number]
  'filter-organism': [organism: string]
}>()

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
