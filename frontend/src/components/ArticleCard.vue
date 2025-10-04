<template>
  <div class="article-card">
    <div class="article-checkbox">
      <input
        type="checkbox"
        :id="`article-${article.id}`"
        :checked="selected"
        @change="$emit('toggle', article.id)"
      />
    </div>
    <div class="article-content">
      <div class="article-tags">
        <FilterTag
          label="Year"
          :value="article.year"
          tag-type="year"
          @click="$emit('filter-year', article.year)"
        />
        <FilterTag
          label="Org"
          :value="article.organism"
          tag-type="organism"
          @click="$emit('filter-organism', article.organism)"
        />
      </div>
      <h3 class="article-title">
        <router-link :to="`/article/${article.id}`" class="title-link">
          {{ article.title }}
        </router-link>
      </h3>
      <p class="article-description">{{ article.description }}</p>
      <div class="article-meta">
        <span class="article-date">{{ formatDate(article.date) }}</span>
        <span class="article-source">{{ article.source }}</span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { Article } from '../types/article'
import FilterTag from './FilterTag.vue'

defineProps<{
  article: Article
  selected: boolean
}>()

defineEmits<{
  'toggle': [id: string]
  'filter-year': [year: number]
  'filter-organism': [organism: string]
}>()

const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}
</script>

<style scoped>
@import '../assets/css/article-card.css';
</style>
