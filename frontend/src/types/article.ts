export interface Article {
  _id?: string
  id?: string
  title: string
  pmcid?: string
  doi?: string
  pubmed_url?: string
  publication_date?: string
  journal_name?: string
  image_url?: string

  abstract?: string
  full_text?: string
  conclusion?: string

  authors?: string[]
  author_affiliations?: string[]

  ai_generated_summary?: string
  key_findings?: string
  future_research_fields?: string
  impact_statement?: string

  study_type?: string
  experimental_platform?: string
  space_environment_stressors?: string[]
  related_papers?: string[]

  primary_organisms_studied?: string[]
  affected_organ_systems?: string[]
  biological_analysis_level?: string[]

  experimental_duration_days?: number
  sample_size?: number
  sampling_methodology?: string

  demonstrates_space_adaptation?: boolean
  identifies_countermeasures?: boolean
  relevant_for_long_duration_missions?: boolean
  health_implications_severity?: string
  reproducibility_level?: string

  applicable_to_missions?: string[]
  space_agency_involvement?: string[]

  // Campos legacy para compatibilidad
  description?: string
  date?: string
  source?: string
  year?: number
  organism?: string
  imageUrl?: string
}

export interface SearchResponse {
  query: string
  total: number
  articles: Article[]
}

export interface SearchFilters {
  query?: string
  year?: number
  organism?: string
  organisms?: string[]
  years?: number[]
  sources?: string[]
  article_types?: string[]
}

export interface FilterOption {
  name: string
  values: (string | number)[]
}

export interface FiltersConfig {
  filters: FilterOption[]
}

export interface SelectedArticle {
  articleId: string
  selected: boolean
}
