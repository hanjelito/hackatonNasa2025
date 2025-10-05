import type { Article, SearchResponse, SearchFilters } from '../types/article'

export const getArticleById = async (id: string): Promise<Article> => {
  try {
    const response = await fetch(`https://vd3ujv7kw1.execute-api.eu-north-1.amazonaws.com/paper/${id}`, {
      method: 'GET',
      headers: {
        'accept': 'application/json'
      }
    })

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }

    const article: Article = await response.json()
    return article
  } catch (error) {
    console.error('Error fetching article by ID:', error)
    throw error
  }
}

export const searchArticles = async (filters: SearchFilters): Promise<SearchResponse> => {
  // Build filters array in the required format
  const filterArray: { name: string; values: (string | number)[] }[] = []

  // Iterate through all filter properties
  Object.keys(filters).forEach(key => {
    if (key !== 'query') {
      const values = filters[key as keyof SearchFilters]
      if (Array.isArray(values) && values.length > 0) {
        // Normalize filter names: lowercase and replace spaces with underscores
        const normalizedName = key.toLowerCase().replace(/\s+/g, '_')
        filterArray.push({ name: normalizedName, values })
      }
    }
  })

  const payload = {
    filters: filterArray,
    query: filters.query || '',
    limit: 10
  }

  try {
    const response = await fetch('https://vd3ujv7kw1.execute-api.eu-north-1.amazonaws.com/paper/search', {
      method: 'POST',
      headers: {
        'accept': 'application/json',
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(payload)
    })

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }

    const articles: Article[] = await response.json()

    // Remove full_text field from each article
    const cleanedArticles = articles.map(({ full_text, ...article }) => article)

    return {
      query: filters.query || '',
      total: cleanedArticles.length,
      articles: cleanedArticles
    }
  } catch (error) {
    console.error('Error fetching articles from API:', error)
    throw error
  }
}
