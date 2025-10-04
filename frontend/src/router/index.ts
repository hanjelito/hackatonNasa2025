import { createRouter, createWebHistory } from 'vue-router'
import SearchView from '../pages/SearchView.vue'
import ArticleDetailView from '../pages/ArticleDetailView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'search',
      component: SearchView
    },
    {
      path: '/article/:id',
      name: 'article-detail',
      component: ArticleDetailView
    }
  ]
})

export default router
