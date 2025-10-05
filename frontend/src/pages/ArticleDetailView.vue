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
            <span v-if="article.publication_date" class="tag tag-year">{{ new Date(article.publication_date).getFullYear() }}</span>
            <span v-if="article.study_type" class="tag tag-organism">{{ article.study_type }}</span>
            <span v-if="article.health_implications_severity" class="tag"
                  :class="{
                    'tag-high': article.health_implications_severity === 'High',
                    'tag-moderate': article.health_implications_severity === 'Moderate to High' || article.health_implications_severity === 'Moderate',
                    'tag-low': article.health_implications_severity === 'Low'
                  }">
              {{ article.health_implications_severity }}
            </span>
          </div>
          <h1 class="article-title">{{ article.title }}</h1>
          <div class="article-meta">
            <span v-if="article.publication_date" class="meta-item">
              <CalendarIcon class="w-5 h-5" />
              {{ formatDate(article.publication_date) }}
            </span>
            <span v-if="article.journal_name" class="meta-item">
              <DocumentTextIcon class="w-5 h-5" />
              {{ article.journal_name }}
            </span>
            <span v-if="article.pmcid" class="meta-item">
              <DocumentTextIcon class="w-5 h-5" />
              {{ article.pmcid }}
            </span>
          </div>

          <!-- Links importantes -->
          <div v-if="article.doi || article.pubmed_url" class="article-links">
            <a v-if="article.doi" :href="`https://doi.org/${article.doi}`" target="_blank" class="external-link">
              DOI: {{ article.doi }}
            </a>
            <a v-if="article.pubmed_url" :href="article.pubmed_url" target="_blank" class="external-link">
              View on PubMed
            </a>
          </div>
        </div>

        <div v-if="article.image_url" class="article-image">
          <img :src="article.image_url" :alt="article.title" />
        </div>

        <div class="article-content">
          <!-- Summary and Impact -->
          <div v-if="article.ai_generated_summary" class="content-section highlight-section">
            <h2>Summary</h2>
            <p>{{ article.ai_generated_summary }}</p>
          </div>

          <div v-if="article.impact_statement" class="content-section highlight-section">
            <h2>Impact Statement</h2>
            <p>{{ article.impact_statement }}</p>
          </div>

          <!-- Abstract -->
          <div v-if="article.abstract" class="content-section">
            <h2>Abstract</h2>
            <p>{{ article.abstract }}</p>
          </div>

          <!-- Key Findings -->
          <div v-if="article.key_findings" class="content-section">
            <h2>Key Findings</h2>
            <p style="white-space: pre-line;">{{ article.key_findings }}</p>
          </div>

          <!-- Full Text -->
          <div v-if="article.full_text" class="content-section">
            <h2>Full Text</h2>
            <p style="white-space: pre-line;">{{ article.full_text }}</p>
          </div>

          <!-- Conclusion -->
          <div v-if="article.conclusion" class="content-section">
            <h2>Conclusion</h2>
            <p>{{ article.conclusion }}</p>
          </div>

          <!-- Study Information -->
          <div v-if="article.experimental_platform || article.experimental_duration_days || article.sample_size" class="content-section info-grid">
            <h2>Study Information</h2>
            <div class="info-items">
              <div v-if="article.experimental_platform" class="info-item">
                <strong>Platform:</strong> {{ article.experimental_platform }}
              </div>
              <div v-if="article.experimental_duration_days" class="info-item">
                <strong>Duration:</strong> {{ article.experimental_duration_days }} days
              </div>
              <div v-if="article.sample_size" class="info-item">
                <strong>Sample Size:</strong> {{ article.sample_size }}
              </div>
              <div v-if="article.sampling_methodology" class="info-item">
                <strong>Methodology:</strong> {{ article.sampling_methodology }}
              </div>
            </div>
          </div>

          <!-- Organisms and Systems -->
          <div v-if="article.primary_organisms_studied && article.primary_organisms_studied.length > 0" class="content-section">
            <h2>Organisms Studied</h2>
            <div class="tag-list">
              <span v-for="organism in article.primary_organisms_studied" :key="organism" class="tag">
                {{ organism }}
              </span>
            </div>
          </div>

          <div v-if="article.affected_organ_systems && article.affected_organ_systems.length > 0" class="content-section">
            <h2>Affected Organ Systems</h2>
            <div class="tag-list">
              <span v-for="system in article.affected_organ_systems" :key="system" class="tag">
                {{ system }}
              </span>
            </div>
          </div>

          <!-- Space Environment Stressors -->
          <div v-if="article.space_environment_stressors && article.space_environment_stressors.length > 0" class="content-section">
            <h2>Space Environment Stressors</h2>
            <div class="tag-list">
              <span v-for="stressor in article.space_environment_stressors" :key="stressor" class="tag tag-stressor">
                {{ stressor }}
              </span>
            </div>
          </div>

          <!-- Mission Applicability -->
          <div v-if="article.applicable_to_missions && article.applicable_to_missions.length > 0" class="content-section">
            <h2>Applicable to Missions</h2>
            <div class="tag-list">
              <span v-for="mission in article.applicable_to_missions" :key="mission" class="tag tag-mission">
                {{ mission }}
              </span>
            </div>
          </div>

          <!-- Space Agencies -->
          <div v-if="article.space_agency_involvement && article.space_agency_involvement.length > 0" class="content-section">
            <h2>Space Agency Involvement</h2>
            <div class="tag-list">
              <span v-for="agency in article.space_agency_involvement" :key="agency" class="tag tag-agency">
                {{ agency }}
              </span>
            </div>
          </div>

          <!-- Future Research -->
          <div v-if="article.future_research_fields" class="content-section">
            <h2>Future Research Fields</h2>
            <p style="white-space: pre-line;">{{ article.future_research_fields }}</p>
          </div>

          <!-- Authors and Affiliations -->
          <div v-if="article.authors && article.authors.length > 0" class="content-section">
            <h2>Authors</h2>
            <div class="authors-list">
              <div v-for="(author, index) in article.authors" :key="author" class="author-item">
                <UserIcon class="w-5 h-5" />
                <div>
                  <span>{{ author }}</span>
                  <span v-if="article.author_affiliations && article.author_affiliations[index]" class="affiliation">
                    {{ article.author_affiliations[index] }}
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div v-else class="loading-state">
        <p>Loading article...</p>
      </div>
    </div>

    <ChatWidget v-if="article" :article-title="article.title" :paper-id="article._id || article.id || article.pmcid || ''" />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import NavHeader from '../components/NavHeader.vue'
import type { Article } from '../types/article'
import mockData from '../data/mockArticleReal.json'
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
  const foundArticle = mockData.papers.find((a: any) =>
    a._id === articleId || a.id === articleId || a.pmcid === articleId
  )
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
