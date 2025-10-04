<template>
  <div class="min-h-screen bg-gray-100 py-8 px-4">
    <div class="max-w-4xl mx-auto">
      <button @click="goBack" class="back-button">
        ← Back to Search
      </button>

      <div v-if="article" class="article-detail">
        <div class="article-header">
          <div class="tags-row">
            <span class="tag tag-year">{{ article.year }}</span>
            <span class="tag tag-organism">{{ article.organism }}</span>
          </div>
          <h1 class="article-title">{{ article.title }}</h1>
          <div class="article-meta">
            <span class="meta-item">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect>
                <line x1="16" y1="2" x2="16" y2="6"></line>
                <line x1="8" y1="2" x2="8" y2="6"></line>
                <line x1="3" y1="10" x2="21" y2="10"></line>
              </svg>
              {{ formatDate(article.date) }}
            </span>
            <span class="meta-item">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path>
              </svg>
              {{ article.source }}
            </span>
          </div>
        </div>

        <div v-if="article.imageUrl" class="article-image">
          <img :src="article.imageUrl" :alt="article.title" />
        </div>

        <div class="article-content">
          <div class="content-section">
            <h2>Overview</h2>
            <p>{{ article.description }}</p>
          </div>

          <div class="content-section">
            <h2>Full Article</h2>
            <p>
              This groundbreaking research represents a significant advancement in our understanding of space exploration and scientific discovery.
              The findings have been meticulously documented and peer-reviewed by leading experts in the field.
            </p>
            <p>
              The implications of this work extend far beyond initial expectations, opening new avenues for future research and exploration.
              Scientists around the world are eagerly analyzing the data and collaborating to build upon these remarkable findings.
            </p>
            <p>
              Further investigations are planned to expand on these initial discoveries, with multiple missions and experiments already in development.
              The international scientific community continues to work together to unlock the mysteries revealed by this important work.
            </p>
          </div>

          <div class="content-section">
            <h2>Authors</h2>
            <div class="authors-list">
              <div v-for="author in article.authors" :key="author" class="author-item">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
                  <circle cx="12" cy="7" r="4"></circle>
                </svg>
                <span>{{ author }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div v-else class="loading-state">
        <p>Loading article...</p>
      </div>
    </div>

    <ChatWidget v-if="article" :article-title="article.title" :paper-id="article.id" />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import type { Article } from '../types/article'
import mockData from '../data/mockArticles.json'
import ChatWidget from '../components/ChatWidget.vue'

const route = useRoute()
const router = useRouter()
const article = ref<Article | null>(null)

onMounted(() => {
  const articleId = route.params.id as string
  const foundArticle = mockData.articles.find((a: Article) => a.id === articleId)
  if (foundArticle) {
    article.value = foundArticle as Article
  }
})

const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}

const goBack = () => {
  // Navegar de vuelta sin perder el estado
  router.back()
}
</script>

<style scoped>
@import '../assets/css/article-detail.css';
</style>
