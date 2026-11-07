
<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import {
  Search,
  RefreshCw,
  ExternalLink,
  Newspaper,
  Clock3,
  AlertCircle,
  Globe2,
  ArrowRight,
} from 'lucide-vue-next'

interface NewsArticle {
  id: number
  title: string
  summary: string
  source_name: string
  source_url: string
  article_url: string
  image_url: string
  category: string
  is_rumour: boolean
  published_at: string | null
}

interface NewsResponse {
  count: number
  next: string | null
  previous: string | null
  results: NewsArticle[]
}

const API_BASE =
  import.meta.env.VITE_API_BASE_URL ||
  'http://127.0.0.1:8000/api/v1'

const articles = ref<NewsArticle[]>([])
const search = ref('')
const selectedCategory = ref('all')

const isLoading = ref(false)
const error = ref('')
const currentPage = ref(1)
const totalArticles = ref(0)
const hasNext = ref(false)
const hasPrevious = ref(false)

const categories = [
  { label: 'All News', value: 'all' },
  { label: 'Breaking', value: 'breaking' },
  { label: 'Transfers', value: 'transfers' },
  { label: 'Matches', value: 'matches' },
  { label: 'Injuries', value: 'injuries' },
  { label: 'Managers', value: 'managers' },
  { label: 'International', value: 'international' },
]

const featuredArticle = computed(() => articles.value[0] || null)

const otherArticles = computed(() => articles.value.slice(1))

const formatDate = (date: string | null) => {
  if (!date) return 'Recently published'

  const parsed = new Date(date)

  if (Number.isNaN(parsed.getTime())) {
    return 'Recently published'
  }

  return new Intl.DateTimeFormat('en', {
    dateStyle: 'medium',
    timeStyle: 'short',
  }).format(parsed)
}

const fetchNews = async (page = 1) => {
  isLoading.value = true
  error.value = ''

  try {
    const params = new URLSearchParams({
      page: String(page),
      page_size: '20',
    })

    if (selectedCategory.value !== 'all') {
      params.set('category', selectedCategory.value)
    }

    if (search.value.trim()) {
      params.set('search', search.value.trim())
    }

    const response = await fetch(
      `${API_BASE}/news/?${params.toString()}`
    )

    if (!response.ok) {
      throw new Error(`News API error: ${response.status}`)
    }

    const data = await response.json()

    // Supports both paginated and unpaginated DRF responses.
    if (Array.isArray(data)) {
      articles.value = data
      totalArticles.value = data.length
      hasNext.value = false
      hasPrevious.value = false
    } else {
      const result = data as NewsResponse

      articles.value = result.results || []
      totalArticles.value = result.count || 0
      hasNext.value = Boolean(result.next)
      hasPrevious.value = Boolean(result.previous)
    }

    currentPage.value = page
  } catch (err) {
    error.value =
      err instanceof Error
        ? err.message
        : 'Unable to load football news.'

  } finally {
    isLoading.value = false
  }
}

const changeCategory = (category: string) => {
  selectedCategory.value = category
  fetchNews(1)
}

const searchNews = () => {
  fetchNews(1)
}

const nextPage = () => {
  if (hasNext.value && !isLoading.value) {
    fetchNews(currentPage.value + 1)
  }
}

const previousPage = () => {
  if (hasPrevious.value && !isLoading.value) {
    fetchNews(currentPage.value - 1)
  }
}

const categoryLabel = (category: string) => {
  return categories.find(item => item.value === category)?.label
    || 'Football'
}

onMounted(() => {
  fetchNews()
})
</script>

<template>
  <main class="min-h-screen bg-[#070A0F] text-[#F5F7FA]">

    <!-- Hero -->
    <section class="border-b border-[#202936]">
      <div class="mx-auto max-w-7xl px-4 py-12 sm:px-6 lg:py-16">

        <div class="flex flex-col justify-between gap-8 lg:flex-row lg:items-end">

          <div>
            <div class="mb-5 flex items-center gap-3">
              <div class="flex h-12 w-12 items-center justify-center rounded-2xl border border-[#B7FF3C]/20 bg-[#B7FF3C]/10">
                <Newspaper class="h-6 w-6 text-[#B7FF3C]" />
              </div>

              <span class="text-sm font-semibold uppercase tracking-[0.25em] text-[#B7FF3C]">
                FIDS Global Coverage
              </span>
            </div>

            <h1 class="text-4xl font-bold tracking-tight sm:text-6xl">
              The World of
              <span class="text-[#B7FF3C]">Football.</span>
            </h1>

            <p class="mt-5 max-w-2xl text-base leading-7 text-[#8993A4]">
              Global football news, transfer updates, match reports,
              player stories and breaking developments from
              international publishers.
            </p>

            <div class="mt-7 flex flex-wrap items-center gap-5 text-sm text-[#8993A4]">
              <span class="flex items-center gap-2">
                <Globe2 class="h-4 w-4 text-[#B7FF3C]" />
                Worldwide coverage
              </span>

              <span class="flex items-center gap-2">
                <Newspaper class="h-4 w-4 text-[#B7FF3C]" />
                Multiple publishers
              </span>
            </div>
          </div>

          <button
            @click="fetchNews(currentPage)"
            :disabled="isLoading"
            class="inline-flex items-center justify-center gap-2 rounded-xl border border-[#202936] bg-[#0F141C] px-5 py-3 text-sm font-semibold transition hover:border-[#B7FF3C] disabled:opacity-50"
          >
            <RefreshCw
              :class="['h-4 w-4', isLoading && 'animate-spin']"
            />
            Refresh News
          </button>

        </div>

      </div>
    </section>

    <div class="mx-auto max-w-7xl px-4 py-10 sm:px-6">

      <!-- Search -->
      <form
        @submit.prevent="searchNews"
        class="mb-7 flex flex-col gap-3 sm:flex-row"
      >
        <div class="relative flex-1">
          <Search class="absolute left-4 top-1/2 h-5 w-5 -translate-y-1/2 text-[#8993A4]" />

          <input
            v-model="search"
            type="search"
            placeholder="Search players, clubs, competitions..."
            class="w-full rounded-xl border border-[#202936] bg-[#0F141C] py-4 pl-12 pr-4 text-sm outline-none transition placeholder:text-[#667085] focus:border-[#B7FF3C]"
          />
        </div>

        <button
          type="submit"
          class="rounded-xl bg-[#B7FF3C] px-7 py-4 font-semibold text-[#070A0F] transition hover:opacity-90"
        >
          Search
        </button>
      </form>

      <!-- Categories -->
      <div class="mb-10 flex gap-2 overflow-x-auto pb-3">
        <button
          v-for="category in categories"
          :key="category.value"
          @click="changeCategory(category.value)"
          class="shrink-0 rounded-xl border px-5 py-3 text-sm font-medium transition"
          :class="
            selectedCategory === category.value
              ? 'border-[#B7FF3C] bg-[#B7FF3C] text-[#070A0F]'
              : 'border-[#202936] bg-[#0F141C] text-[#8993A4] hover:border-[#B7FF3C]'
          "
        >
          {{ category.label }}
        </button>
      </div>

      <!-- Loading -->
      <div
        v-if="isLoading"
        class="grid gap-5 md:grid-cols-2 lg:grid-cols-3"
      >
        <div
          v-for="i in 6"
          :key="i"
          class="h-72 animate-pulse rounded-2xl border border-[#202936] bg-[#0F141C]"
        />
      </div>

      <!-- Error -->
      <div
        v-else-if="error"
        class="rounded-2xl border border-red-500/30 bg-red-500/5 p-8 text-center"
      >
        <AlertCircle class="mx-auto mb-4 h-9 w-9 text-red-400" />

        <h3 class="font-semibold">Unable to load football news</h3>

        <p class="mt-2 text-sm text-[#8993A4]">
          {{ error }}
        </p>

        <button
          @click="fetchNews(currentPage)"
          class="mt-5 rounded-xl bg-[#B7FF3C] px-5 py-3 font-semibold text-[#070A0F]"
        >
          Try Again
        </button>
      </div>

      <!-- Empty -->
      <div
        v-else-if="!articles.length"
        class="rounded-2xl border border-[#202936] bg-[#0F141C] py-20 text-center"
      >
        <Newspaper class="mx-auto h-12 w-12 text-[#8993A4]" />

        <h3 class="mt-5 text-xl font-semibold">
          No articles found
        </h3>

        <p class="mt-2 text-sm text-[#8993A4]">
          Try another search or category.
        </p>
      </div>

      <template v-else>

        <!-- Featured -->
        <section
          v-if="currentPage === 1 && !search && selectedCategory === 'all' && featuredArticle"
          class="mb-12"
        >
          <div class="mb-5 flex items-center justify-between">
            <h2 class="text-xl font-bold">Top Story</h2>

            <span class="text-xs font-semibold uppercase tracking-widest text-[#B7FF3C]">
              Featured
            </span>
          </div>

          <a
            :href="featuredArticle.article_url"
            target="_blank"
            rel="noopener noreferrer"
            class="group grid overflow-hidden rounded-3xl border border-[#202936] bg-[#0F141C] lg:grid-cols-2"
          >
            <div class="relative min-h-64 overflow-hidden bg-[#151C26] lg:min-h-[380px]">
              <img
                v-if="featuredArticle.image_url"
                :src="featuredArticle.image_url"
                :alt="featuredArticle.title"
                class="absolute inset-0 h-full w-full object-cover transition duration-500 group-hover:scale-105"
              />

              <div class="absolute inset-0 bg-gradient-to-t from-black/80 via-transparent to-transparent" />

              <span class="absolute bottom-5 left-5 rounded-lg bg-[#B7FF3C] px-3 py-2 text-xs font-bold text-[#070A0F]">
                {{ categoryLabel(featuredArticle.category) }}
              </span>
            </div>

            <div class="flex flex-col justify-center p-7 sm:p-10">
              <span class="text-xs font-bold uppercase tracking-widest text-[#B7FF3C]">
                {{ featuredArticle.source_name }}
              </span>

              <h3 class="mt-5 text-2xl font-bold leading-tight sm:text-3xl">
                {{ featuredArticle.title }}
              </h3>

              <p class="mt-5 line-clamp-4 leading-7 text-[#8993A4]">
                {{ featuredArticle.summary }}
              </p>

              <div class="mt-8 flex flex-wrap items-center justify-between gap-4 text-xs text-[#8993A4]">
                <span class="flex items-center gap-2">
                  <Clock3 class="h-4 w-4" />
                  {{ formatDate(featuredArticle.published_at) }}
                </span>

                <span class="flex items-center gap-2 font-semibold text-[#B7FF3C]">
                  Read Full Story
                  <ExternalLink class="h-4 w-4" />
                </span>
              </div>
            </div>
          </a>
        </section>

        <!-- Articles -->
        <section>
          <div class="mb-6 flex items-center justify-between">
            <div>
              <h2 class="text-xl font-bold">Latest Football News</h2>

              <p class="mt-1 text-sm text-[#8993A4]">
                {{ totalArticles }} articles available
              </p>
            </div>
          </div>

          <div class="grid gap-5 sm:grid-cols-2 lg:grid-cols-3">

            <article
              v-for="article in (
                currentPage === 1 && !search && selectedCategory === 'all'
                  ? otherArticles
                  : articles
              )"
              :key="article.id"
              class="group overflow-hidden rounded-2xl border border-[#202936] bg-[#0F141C] transition hover:-translate-y-1 hover:border-[#B7FF3C]/50"
            >
              <a
                :href="article.article_url"
                target="_blank"
                rel="noopener noreferrer"
                class="block"
              >
                <div class="relative h-48 overflow-hidden bg-[#151C26]">
                  <img
                    v-if="article.image_url"
                    :src="article.image_url"
                    :alt="article.title"
                    loading="lazy"
                    class="h-full w-full object-cover transition duration-500 group-hover:scale-105"
                  />

                  <div
                    v-else
                    class="flex h-full items-center justify-center"
                  >
                    <Newspaper class="h-12 w-12 text-[#667085]" />
                  </div>

                  <span class="absolute left-4 top-4 rounded-lg bg-[#070A0F]/90 px-3 py-2 text-xs font-semibold text-[#B7FF3C]">
                    {{ categoryLabel(article.category) }}
                  </span>
                </div>

                <div class="p-5">

                  <div class="mb-3 flex flex-wrap items-center gap-2 text-xs">
                    <span class="font-bold text-[#B7FF3C]">
                      {{ article.source_name }}
                    </span>

                    <span
                      v-if="article.is_rumour"
                      class="rounded-md border border-orange-400/30 bg-orange-400/10 px-2 py-1 text-orange-300"
                    >
                      Rumour
                    </span>
                  </div>

                  <h3 class="line-clamp-2 min-h-14 text-lg font-bold leading-7 transition group-hover:text-[#B7FF3C]">
                    {{ article.title }}
                  </h3>

                  <p class="mt-3 line-clamp-3 text-sm leading-6 text-[#8993A4]">
                    {{ article.summary || 'Read the original article for more details.' }}
                  </p>

                  <div class="mt-6 flex items-center justify-between border-t border-[#202936] pt-4 text-xs text-[#8993A4]">
                    <span>
                      {{ formatDate(article.published_at) }}
                    </span>

                    <ExternalLink class="h-4 w-4 transition group-hover:text-[#B7FF3C]" />
                  </div>

                </div>
              </a>
            </article>

          </div>
        </section>

        <!-- Pagination -->
        <div class="mt-12 flex items-center justify-center gap-4">
          <button
            @click="previousPage"
            :disabled="!hasPrevious || isLoading"
            class="rounded-xl border border-[#202936] px-5 py-3 text-sm font-semibold transition hover:border-[#B7FF3C] disabled:cursor-not-allowed disabled:opacity-30"
          >
            Previous
          </button>

          <span class="text-sm text-[#8993A4]">
            Page {{ currentPage }}
          </span>

          <button
            @click="nextPage"
            :disabled="!hasNext || isLoading"
            class="flex items-center gap-2 rounded-xl bg-[#B7FF3C] px-5 py-3 text-sm font-semibold text-[#070A0F] disabled:cursor-not-allowed disabled:opacity-30"
          >
            Next
            <ArrowRight class="h-4 w-4" />
          </button>
        </div>

      </template>
    </div>
  </main>
</template>
