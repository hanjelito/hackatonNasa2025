<template>
  <div class="article-detail-view">
    <NavHeader />

    <div class="detail-container">
      <button @click="goBack" class="back-button">
        <ArrowLeftIcon class="w-5 h-5" />
        <span>Back to Search</span>
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
              <CalendarIcon class="w-5 h-5" />
              {{ formatDate(article.date) }}
            </span>
            <span class="meta-item">
              <DocumentTextIcon class="w-5 h-5" />
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
                <UserIcon class="w-5 h-5" />
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
import NavHeader from '../components/NavHeader.vue'
import type { Article } from '../types/article'
import mockData from '../data/mockArticles.json'
import ChatWidget from '../components/ChatWidget.vue'
import CalendarIcon from '../components/icons/CalendarIcon.vue'
import DocumentTextIcon from '../components/icons/DocumentTextIcon.vue'
import UserIcon from '../components/icons/UserIcon.vue'
import ArrowLeftIcon from '../components/icons/ArrowLeftIcon.vue'

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
