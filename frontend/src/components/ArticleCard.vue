<template>
  <div class="article-card">
    <div class="article-checkbox">
      <input
        type="checkbox"
        :id="`article-${getArticleId(article)}`"
        :checked="selected"
        @change="$emit('toggle', getArticleId(article))"
      />
    </div>
    <div class="article-content">
      <div class="article-tags">
        <FilterTag
          v-if="article.publication_date"
          label="Year"
          :value="new Date(article.publication_date).getFullYear()"
          tag-type="year"
          @click="$emit('filter-year', new Date(article.publication_date).getFullYear())"
        />
        <FilterTag
          v-if="article.primary_organisms_studied && article.primary_organisms_studied.length > 0"
          label="Org"
          :value="article.primary_organisms_studied[0]"
          tag-type="organism"
          @click="$emit('filter-organism', article.primary_organisms_studied[0])"
        />
      </div>
      <h3 class="article-title">
        <router-link :to="`/article/${getArticleId(article)}`" class="title-link">
          {{ article.title }}
        </router-link>
      </h3>
      <p class="article-description">{{ article.abstract || article.ai_generated_summary || 'No description available' }}</p>
      <div class="article-meta">
        <span v-if="article.publication_date" class="article-date">
          <CalendarIcon class="w-4 h-4" />
          {{ formatDate(article.publication_date) }}
        </span>
        <span v-if="article.journal_name" class="article-source">
          <BookmarkIcon class="w-4 h-4" />
          {{ article.journal_name }}
        </span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { Article } from '../types/article'
import FilterTag from './FilterTag.vue'
import CalendarIcon from './icons/CalendarIcon.vue'
import BookmarkIcon from './icons/BookmarkIcon.vue'

defineProps<{
  article: Article
  selected: boolean
}>()

defineEmits<{
  'toggle': [id: string]
  'filter-year': [year: number]
  'filter-organism': [organism: string]
}>()

const getArticleId = (article: Article): string => {
  return article._id || article.id || article.pmcid || ''
}

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
