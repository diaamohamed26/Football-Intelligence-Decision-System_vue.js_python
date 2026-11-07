
<script setup lang="ts">
import { computed, ref } from 'vue'

type NewsStatus = 'Published' | 'Draft' | 'Scheduled'
type NewsCategory =
  | 'Transfers'
  | 'Match Reports'
  | 'Premier League'
  | 'Champions League'
  | 'Analysis'
  | 'Injuries'

interface NewsArticle {
  id: number
  title: string
  excerpt: string
  category: NewsCategory
  author: string
  source: string
  status: NewsStatus
  publishedAt: string
  views: number
  featured: boolean
  image: string
}

const categories: NewsCategory[] = [
  'Transfers',
  'Match Reports',
  'Premier League',
  'Champions League',
  'Analysis',
  'Injuries',
]

const articles = ref<NewsArticle[]>([
  {
    id: 1,
    title: 'Champions League: Tactical Analysis of the Latest Fixtures',
    excerpt: 'A detailed look at the key tactical decisions and performances.',
    category: 'Champions League',
    author: 'FIDS Editorial',
    source: 'FIDS News',
    status: 'Published',
    publishedAt: '2026-10-10T10:30',
    views: 12480,
    featured: true,
    image: 'https://images.unsplash.com/photo-1522778119026-d647f0596c20?auto=format&fit=crop&w=160&q=80',
  },
  {
    id: 2,
    title: 'Transfer Watch: Players to Follow This Season',
    excerpt: 'Scouting reports identify promising players across European leagues.',
    category: 'Transfers',
    author: 'Ahmed Hassan',
    source: 'FIDS Scouting',
    status: 'Published',
    publishedAt: '2026-10-09T14:15',
    views: 8630,
    featured: false,
    image: 'https://images.unsplash.com/photo-1574629810360-7efbbe195018?auto=format&fit=crop&w=160&q=80',
  },
  {
    id: 3,
    title: 'Premier League: The Numbers Behind the Title Race',
    excerpt: 'Expected goals, pressing intensity, and defensive performance.',
    category: 'Premier League',
    author: 'Mohamed Ali',
    source: 'FIDS Analytics',
    status: 'Draft',
    publishedAt: '2026-10-11T12:00',
    views: 0,
    featured: false,
    image: 'https://images.unsplash.com/photo-1508098682722-e99c43a406b2?auto=format&fit=crop&w=160&q=80',
  },
  {
    id: 4,
    title: 'Match Preview: Key Battles and Expected Lineups',
    excerpt: 'Our preview covers player availability and tactical matchups.',
    category: 'Match Reports',
    author: 'FIDS Editorial',
    source: 'FIDS News',
    status: 'Scheduled',
    publishedAt: '2026-10-12T18:00',
    views: 0,
    featured: false,
    image: 'https://images.unsplash.com/photo-1459865264687-595d652de67e?auto=format&fit=crop&w=160&q=80',
  },
  {
    id: 5,
    title: 'Injury Update: Important Players Return to Training',
    excerpt: 'The latest availability updates ahead of the upcoming fixtures.',
    category: 'Injuries',
    author: 'Sara Mahmoud',
    source: 'FIDS News',
    status: 'Published',
    publishedAt: '2026-10-08T09:00',
    views: 5720,
    featured: false,
    image: 'https://images.unsplash.com/photo-1517466787929-bc90951d0974?auto=format&fit=crop&w=160&q=80',
  },
  {
    id: 6,
    title: 'How Modern Pressing Shapes Football Matches',
    excerpt: 'An analytical breakdown of pressing systems and their impact.',
    category: 'Analysis',
    author: 'Ahmed Hassan',
    source: 'FIDS Analytics',
    status: 'Draft',
    publishedAt: '2026-10-10T16:00',
    views: 0,
    featured: false,
    image: 'https://images.unsplash.com/photo-1431324155629-1a6deb1dec8d?auto=format&fit=crop&w=160&q=80',
  },
])

const search = ref('')
const statusFilter = ref<'All' | NewsStatus>('All')
const categoryFilter = ref<'All' | NewsCategory>('All')
const showEditor = ref(false)
const showDetails = ref(false)
const editingId = ref<number | null>(null)
const selectedArticle = ref<NewsArticle | null>(null)
const formError = ref('')

const emptyForm = (): Omit<NewsArticle, 'id' | 'views'> => ({
  title: '',
  excerpt: '',
  category: 'Analysis',
  author: 'FIDS Editorial',
  source: 'FIDS News',
  status: 'Draft',
  publishedAt: new Date().toISOString().slice(0, 16),
  featured: false,
  image: '',
})

const form = ref<Omit<NewsArticle, 'id' | 'views'>>(emptyForm())

const publishedCount = computed(
  () => articles.value.filter((item) => item.status === 'Published').length,
)
const draftCount = computed(
  () => articles.value.filter((item) => item.status === 'Draft').length,
)
const scheduledCount = computed(
  () => articles.value.filter((item) => item.status === 'Scheduled').length,
)
const totalViews = computed(
  () => articles.value.reduce((sum, item) => sum + item.views, 0),
)

const filteredArticles = computed(() => {
  const term = search.value.trim().toLowerCase()

  return articles.value
    .filter((item) => {
      const matchesSearch =
        !term ||
        item.title.toLowerCase().includes(term) ||
        item.author.toLowerCase().includes(term) ||
        item.source.toLowerCase().includes(term)

      const matchesStatus =
        statusFilter.value === 'All' || item.status === statusFilter.value

      const matchesCategory =
        categoryFilter.value === 'All' ||
        item.category === categoryFilter.value

      return matchesSearch && matchesStatus && matchesCategory
    })
    .sort(
      (a, b) =>
        new Date(b.publishedAt).getTime() -
        new Date(a.publishedAt).getTime(),
    )
})

function formatDate(value: string) {
  if (!value) return '—'

  return new Date(value).toLocaleString('en-GB', {
    day: '2-digit',
    month: 'short',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  })
}

function formatViews(value: number) {
  return new Intl.NumberFormat('en-US', {
    notation: value >= 1000 ? 'compact' : 'standard',
    maximumFractionDigits: 1,
  }).format(value)
}

function statusClass(status: NewsStatus) {
  const styles: Record<NewsStatus, string> = {
    Published: 'bg-emerald-500/10 text-emerald-400 ring-emerald-500/20',
    Draft: 'bg-amber-500/10 text-amber-400 ring-amber-500/20',
    Scheduled: 'bg-sky-500/10 text-sky-400 ring-sky-500/20',
  }

  return styles[status]
}

function openCreate() {
  editingId.value = null
  form.value = emptyForm()
  formError.value = ''
  showEditor.value = true
}

function openEdit(article: NewsArticle) {
  editingId.value = article.id
  const { id, views, ...editable } = article
  form.value = { ...editable }
  formError.value = ''
  showEditor.value = true
}

function saveArticle() {
  formError.value = ''

  if (!form.value.title.trim()) {
    formError.value = 'Please enter a news title.'
    return
  }

  if (!form.value.author.trim()) {
    formError.value = 'Please enter the author name.'
    return
  }

  if (!form.value.publishedAt) {
    formError.value = 'Please select a publication date.'
    return
  }

  if (editingId.value !== null) {
    const index = articles.value.findIndex(
      (item) => item.id === editingId.value,
    )

    if (index !== -1) {
      const existing = articles.value[index]
      articles.value[index] = {
        ...existing,
        ...form.value,
        title: form.value.title.trim(),
        author: form.value.author.trim(),
        views: existing.views,
      }
    }
  } else {
    const newArticle: NewsArticle = {
      ...form.value,
      id: Math.max(0, ...articles.value.map((item) => item.id)) + 1,
      title: form.value.title.trim(),
      author: form.value.author.trim(),
      views: 0,
    }

    articles.value.unshift(newArticle)
  }

  showEditor.value = false
}

function viewArticle(article: NewsArticle) {
  selectedArticle.value = article
  showDetails.value = true
}

function deleteArticle(article: NewsArticle) {
  const confirmed = window.confirm(
    `Delete "${article.title}"? This action cannot be undone.`,
  )

  if (!confirmed) return

  articles.value = articles.value.filter((item) => item.id !== article.id)

  if (selectedArticle.value?.id === article.id) {
    selectedArticle.value = null
    showDetails.value = false
  }
}

function toggleFeatured(article: NewsArticle) {
  article.featured = !article.featured
}

function closeEditor() {
  showEditor.value = false
  formError.value = ''
}
</script>

<template>
  <div class="min-h-screen bg-slate-950 px-4 py-6 text-slate-100 sm:px-6 lg:px-8">
    <div class="mx-auto max-w-7xl space-y-7">
      <!-- Page heading -->
      <header class="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
        <div>
          <div class="mb-2 flex items-center gap-2 text-sm text-slate-400">
            <span>Admin</span>
            <span>/</span>
            <span class="text-emerald-400">News</span>
          </div>

          <h1 class="text-3xl font-bold tracking-tight text-white">
            News Management
          </h1>

          <p class="mt-2 text-sm text-slate-400">
            Create, edit, and manage football news articles.
          </p>
        </div>

        <button
          type="button"
          @click="openCreate"
          class="inline-flex items-center justify-center gap-2 rounded-xl bg-emerald-500 px-5 py-3 text-sm font-semibold text-slate-950 transition hover:bg-emerald-400"
        >
          <span class="text-lg leading-none">+</span>
          Create article
        </button>
      </header>

      <!-- Statistics -->
      <section class="grid grid-cols-1 gap-4 sm:grid-cols-2 xl:grid-cols-4">
        <article class="rounded-2xl border border-slate-800 bg-slate-900 p-5">
          <div class="flex items-center justify-between">
            <p class="text-sm text-slate-400">Total articles</p>
            <span class="rounded-lg bg-violet-500/10 p-2 text-violet-400">▤</span>
          </div>
          <p class="mt-4 text-3xl font-bold text-white">{{ articles.length }}</p>
          <p class="mt-2 text-xs text-slate-500">All news content</p>
        </article>

        <article class="rounded-2xl border border-slate-800 bg-slate-900 p-5">
          <div class="flex items-center justify-between">
            <p class="text-sm text-slate-400">Published</p>
            <span class="rounded-lg bg-emerald-500/10 p-2 text-emerald-400">✓</span>
          </div>
          <p class="mt-4 text-3xl font-bold text-white">{{ publishedCount }}</p>
          <p class="mt-2 text-xs text-emerald-400">Live articles</p>
        </article>

        <article class="rounded-2xl border border-slate-800 bg-slate-900 p-5">
          <div class="flex items-center justify-between">
            <p class="text-sm text-slate-400">Drafts</p>
            <span class="rounded-lg bg-amber-500/10 p-2 text-amber-400">✎</span>
          </div>
          <p class="mt-4 text-3xl font-bold text-white">{{ draftCount }}</p>
          <p class="mt-2 text-xs text-amber-400">Awaiting publication</p>
        </article>

        <article class="rounded-2xl border border-slate-800 bg-slate-900 p-5">
          <div class="flex items-center justify-between">
            <p class="text-sm text-slate-400">Total views</p>
            <span class="rounded-lg bg-sky-500/10 p-2 text-sky-400">◉</span>
          </div>
          <p class="mt-4 text-3xl font-bold text-white">{{ formatViews(totalViews) }}</p>
          <p class="mt-2 text-xs text-sky-400">{{ scheduledCount }} scheduled articles</p>
        </article>
      </section>

      <!-- News table -->
      <section class="overflow-hidden rounded-2xl border border-slate-800 bg-slate-900">
        <div class="border-b border-slate-800 p-5">
          <div class="flex flex-col gap-4 xl:flex-row xl:items-center xl:justify-between">
            <div>
              <h2 class="text-lg font-semibold text-white">All articles</h2>
              <p class="mt-1 text-sm text-slate-400">
                {{ filteredArticles.length }} results found
              </p>
            </div>

            <div class="grid grid-cols-1 gap-3 sm:grid-cols-2 xl:flex">
              <div class="relative">
                <span class="pointer-events-none absolute left-3 top-1/2 -translate-y-1/2 text-slate-500">⌕</span>
                <input
                  v-model="search"
                  type="search"
                  placeholder="Search articles..."
                  class="w-full rounded-xl border border-slate-700 bg-slate-950 py-2.5 pl-9 pr-3 text-sm text-white outline-none placeholder:text-slate-500 focus:border-emerald-500 xl:w-64"
                />
              </div>

              <select
                v-model="statusFilter"
                class="rounded-xl border border-slate-700 bg-slate-950 px-3 py-2.5 text-sm text-slate-200 outline-none focus:border-emerald-500"
              >
                <option value="All">All statuses</option>
                <option value="Published">Published</option>
                <option value="Draft">Draft</option>
                <option value="Scheduled">Scheduled</option>
              </select>

              <select
                v-model="categoryFilter"
                class="rounded-xl border border-slate-700 bg-slate-950 px-3 py-2.5 text-sm text-slate-200 outline-none focus:border-emerald-500"
              >
                <option value="All">All categories</option>
                <option v-for="category in categories" :key="category" :value="category">
                  {{ category }}
                </option>
              </select>
            </div>
          </div>
        </div>

        <div class="overflow-x-auto">
          <table class="w-full min-w-[1000px] text-left">
            <thead class="bg-slate-950/70 text-xs uppercase tracking-wider text-slate-500">
              <tr>
                <th class="px-5 py-4 font-medium">Article</th>
                <th class="px-5 py-4 font-medium">Category</th>
                <th class="px-5 py-4 font-medium">Author</th>
                <th class="px-5 py-4 font-medium">Status</th>
                <th class="px-5 py-4 font-medium">Views</th>
                <th class="px-5 py-4 font-medium">Publication date</th>
                <th class="px-5 py-4 text-right font-medium">Actions</th>
              </tr>
            </thead>

            <tbody class="divide-y divide-slate-800">
              <tr
                v-for="article in filteredArticles"
                :key="article.id"
                class="transition hover:bg-slate-800/40"
              >
                <td class="px-5 py-4">
                  <div class="flex items-center gap-3">
                    <img
                      v-if="article.image"
                      :src="article.image"
                      :alt="article.title"
                      class="h-12 w-16 shrink-0 rounded-lg border border-slate-700 object-cover"
                    />
                    <div v-else class="flex h-12 w-16 shrink-0 items-center justify-center rounded-lg bg-slate-800 text-slate-500">
                      ▤
                    </div>

                    <div class="max-w-xs">
                      <div class="flex flex-wrap items-center gap-2">
                        <p class="line-clamp-2 text-sm font-semibold text-white">
                          {{ article.title }}
                        </p>
                        <span
                          v-if="article.featured"
                          class="rounded-md bg-amber-500/10 px-1.5 py-0.5 text-[10px] font-semibold text-amber-400"
                        >
                          FEATURED
                        </span>
                      </div>
                      <p class="mt-1 text-xs text-slate-500">{{ article.source }}</p>
                    </div>
                  </div>
                </td>

                <td class="px-5 py-4">
                  <span class="rounded-lg border border-slate-700 bg-slate-800/70 px-2.5 py-1.5 text-xs text-slate-300">
                    {{ article.category }}
                  </span>
                </td>

                <td class="px-5 py-4 text-sm text-slate-300">{{ article.author }}</td>

                <td class="px-5 py-4">
                  <span
                    class="inline-flex rounded-full px-2.5 py-1 text-xs font-medium ring-1 ring-inset"
                    :class="statusClass(article.status)"
                  >
                    {{ article.status }}
                  </span>
                </td>

                <td class="px-5 py-4 text-sm tabular-nums text-slate-300">
                  {{ formatViews(article.views) }}
                </td>

                <td class="px-5 py-4 text-xs text-slate-400">
                  {{ formatDate(article.publishedAt) }}
                </td>

                <td class="px-5 py-4">
                  <div class="flex items-center justify-end gap-1">
                    <button
                      type="button"
                      title="View article"
                      @click="viewArticle(article)"
                      class="rounded-lg px-2.5 py-2 text-xs text-slate-300 transition hover:bg-slate-700 hover:text-white"
                    >
                      View
                    </button>
                    <button
                      type="button"
                      title="Edit article"
                      @click="openEdit(article)"
                      class="rounded-lg px-2.5 py-2 text-xs text-emerald-400 transition hover:bg-emerald-500/10"
                    >
                      Edit
                    </button>
                    <button
                      type="button"
                      title="Toggle featured"
                      @click="toggleFeatured(article)"
                      class="rounded-lg px-2.5 py-2 text-xs text-amber-400 transition hover:bg-amber-500/10"
                    >
                      {{ article.featured ? 'Unfeature' : 'Feature' }}
                    </button>
                    <button
                      type="button"
                      title="Delete article"
                      @click="deleteArticle(article)"
                      class="rounded-lg px-2.5 py-2 text-xs text-rose-400 transition hover:bg-rose-500/10"
                    >
                      Delete
                    </button>
                  </div>
                </td>
              </tr>

              <tr v-if="filteredArticles.length === 0">
                <td colspan="7" class="px-5 py-16 text-center">
                  <div class="text-3xl text-slate-600">⌕</div>
                  <p class="mt-3 font-medium text-white">No articles found</p>
                  <p class="mt-1 text-sm text-slate-500">
                    Try changing your search or filters.
                  </p>
                  <button
                    type="button"
                    @click="search = ''; statusFilter = 'All'; categoryFilter = 'All'"
                    class="mt-4 text-sm font-medium text-emerald-400 hover:text-emerald-300"
                  >
                    Clear filters
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <div class="flex flex-col gap-2 border-t border-slate-800 px-5 py-4 text-xs text-slate-500 sm:flex-row sm:items-center sm:justify-between">
          <p>Showing {{ filteredArticles.length }} of {{ articles.length }} articles</p>
          <p>FIDS Admin · News Management</p>
        </div>
      </section>
    </div>

    <!-- Create / Edit modal -->
    <div
      v-if="showEditor"
      class="fixed inset-0 z-50 flex items-center justify-center overflow-y-auto bg-black/70 p-4 backdrop-blur-sm"
      @click.self="closeEditor"
      @keydown.esc="closeEditor"
    >
      <section class="my-auto max-h-[92vh] w-full max-w-2xl overflow-y-auto rounded-2xl border border-slate-700 bg-slate-900 shadow-2xl">
        <header class="sticky top-0 z-10 flex items-center justify-between border-b border-slate-800 bg-slate-900 px-6 py-5">
          <div>
            <h2 class="text-xl font-bold text-white">
              {{ editingId !== null ? 'Edit article' : 'Create article' }}
            </h2>
            <p class="mt-1 text-sm text-slate-400">Enter the article information below.</p>
          </div>
          <button type="button" @click="closeEditor" class="rounded-lg px-3 py-2 text-slate-400 hover:bg-slate-800 hover:text-white">
            ✕
          </button>
        </header>

        <form class="space-y-5 p-6" @submit.prevent="saveArticle">
          <div>
            <label class="mb-2 block text-sm font-medium text-slate-300">Title *</label>
            <input
              v-model="form.title"
              required
              maxlength="200"
              placeholder="Enter a clear news headline"
              class="w-full rounded-xl border border-slate-700 bg-slate-950 px-4 py-3 text-sm text-white outline-none placeholder:text-slate-600 focus:border-emerald-500"
            />
          </div>

          <div>
            <label class="mb-2 block text-sm font-medium text-slate-300">Excerpt</label>
            <textarea
              v-model="form.excerpt"
              rows="3"
              maxlength="500"
              placeholder="Write a short summary..."
              class="w-full resize-y rounded-xl border border-slate-700 bg-slate-950 px-4 py-3 text-sm text-white outline-none placeholder:text-slate-600 focus:border-emerald-500"
            />
          </div>

          <div class="grid grid-cols-1 gap-5 sm:grid-cols-2">
            <div>
              <label class="mb-2 block text-sm font-medium text-slate-300">Category *</label>
              <select
                v-model="form.category"
                required
                class="w-full rounded-xl border border-slate-700 bg-slate-950 px-3 py-3 text-sm text-white outline-none focus:border-emerald-500"
              >
                <option v-for="category in categories" :key="category" :value="category">
                  {{ category }}
                </option>
              </select>
            </div>

            <div>
              <label class="mb-2 block text-sm font-medium text-slate-300">Status *</label>
              <select
                v-model="form.status"
                required
                class="w-full rounded-xl border border-slate-700 bg-slate-950 px-3 py-3 text-sm text-white outline-none focus:border-emerald-500"
              >
                <option value="Draft">Draft</option>
                <option value="Published">Published</option>
                <option value="Scheduled">Scheduled</option>
              </select>
            </div>

            <div>
              <label class="mb-2 block text-sm font-medium text-slate-300">Author *</label>
              <input
                v-model="form.author"
                required
                placeholder="Author name"
                class="w-full rounded-xl border border-slate-700 bg-slate-950 px-4 py-3 text-sm text-white outline-none focus:border-emerald-500"
              />
            </div>

            <div>
              <label class="mb-2 block text-sm font-medium text-slate-300">Source</label>
              <input
                v-model="form.source"
                placeholder="FIDS News"
                class="w-full rounded-xl border border-slate-700 bg-slate-950 px-4 py-3 text-sm text-white outline-none focus:border-emerald-500"
              />
            </div>

            <div>
              <label class="mb-2 block text-sm font-medium text-slate-300">Publication date *</label>
              <input
                v-model="form.publishedAt"
                type="datetime-local"
                required
                class="w-full rounded-xl border border-slate-700 bg-slate-950 px-3 py-3 text-sm text-white outline-none focus:border-emerald-500"
              />
            </div>

            <div>
              <label class="mb-2 block text-sm font-medium text-slate-300">Image URL</label>
              <input
                v-model="form.image"
                type="url"
                placeholder="https://..."
                class="w-full rounded-xl border border-slate-700 bg-slate-950 px-4 py-3 text-sm text-white outline-none focus:border-emerald-500"
              />
            </div>
          </div>

          <label class="flex cursor-pointer items-center gap-3 rounded-xl border border-slate-800 bg-slate-950/70 p-4">
            <input
              v-model="form.featured"
              type="checkbox"
              class="h-4 w-4 accent-emerald-500"
            />
            <span>
              <span class="block text-sm font-medium text-white">Featured article</span>
              <span class="mt-1 block text-xs text-slate-500">Highlight this article in the news section.</span>
            </span>
          </label>

          <p
            v-if="formError"
            class="rounded-lg border border-rose-500/20 bg-rose-500/10 px-4 py-3 text-sm text-rose-300"
          >
            {{ formError }}
          </p>

          <footer class="flex flex-col-reverse gap-3 border-t border-slate-800 pt-5 sm:flex-row sm:justify-end">
            <button
              type="button"
              @click="closeEditor"
              class="rounded-xl border border-slate-700 px-5 py-3 text-sm font-medium text-slate-300 transition hover:bg-slate-800"
            >
              Cancel
            </button>
            <button
              type="submit"
              class="rounded-xl bg-emerald-500 px-5 py-3 text-sm font-semibold text-slate-950 transition hover:bg-emerald-400"
            >
              {{ editingId !== null ? 'Save changes' : 'Create article' }}
            </button>
          </footer>
        </form>
      </section>
    </div>

    <!-- Article details modal -->
    <div
      v-if="showDetails && selectedArticle"
      class="fixed inset-0 z-50 flex items-center justify-center overflow-y-auto bg-black/70 p-4 backdrop-blur-sm"
      @click.self="showDetails = false"
      @keydown.esc="showDetails = false"
    >
      <article class="my-auto w-full max-w-2xl overflow-hidden rounded-2xl border border-slate-700 bg-slate-900 shadow-2xl">
        <div class="relative">
          <img
            v-if="selectedArticle.image"
            :src="selectedArticle.image"
            :alt="selectedArticle.title"
            class="h-56 w-full object-cover"
          />
          <div v-else class="flex h-40 items-center justify-center bg-slate-800 text-slate-500">
            No image available
          </div>
          <button
            type="button"
            @click="showDetails = false"
            class="absolute right-4 top-4 rounded-lg bg-slate-950/80 px-3 py-2 text-white hover:bg-slate-800"
          >
            ✕
          </button>
        </div>

        <div class="space-y-5 p-6">
          <div class="flex flex-wrap items-center gap-2">
            <span class="rounded-lg bg-slate-800 px-3 py-1.5 text-xs text-slate-300">
              {{ selectedArticle.category }}
            </span>
            <span
              class="inline-flex rounded-full px-2.5 py-1 text-xs font-medium ring-1 ring-inset"
              :class="statusClass(selectedArticle.status)"
            >
              {{ selectedArticle.status }}
            </span>
            <span v-if="selectedArticle.featured" class="text-xs font-semibold text-amber-400">
              ★ Featured
            </span>
          </div>

          <h2 class="text-2xl font-bold leading-snug text-white">
            {{ selectedArticle.title }}
          </h2>

          <p class="text-sm leading-7 text-slate-300">
            {{ selectedArticle.excerpt || 'No excerpt has been added to this article yet.' }}
          </p>

          <div class="grid grid-cols-2 gap-4 rounded-xl border border-slate-800 bg-slate-950/60 p-4 sm:grid-cols-4">
            <div>
              <p class="text-xs text-slate-500">Author</p>
              <p class="mt-1 text-sm font-medium text-white">{{ selectedArticle.author }}</p>
            </div>
            <div>
              <p class="text-xs text-slate-500">Source</p>
              <p class="mt-1 text-sm font-medium text-white">{{ selectedArticle.source || '—' }}</p>
            </div>
            <div>
              <p class="text-xs text-slate-500">Views</p>
              <p class="mt-1 text-sm font-medium text-white">{{ formatViews(selectedArticle.views) }}</p>
            </div>
            <div>
              <p class="text-xs text-slate-500">Date</p>
              <p class="mt-1 text-sm font-medium text-white">{{ formatDate(selectedArticle.publishedAt) }}</p>
            </div>
          </div>

          <div class="flex justify-end gap-3 border-t border-slate-800 pt-5">
            <button
              type="button"
              @click="showDetails = false"
              class="rounded-xl border border-slate-700 px-4 py-2.5 text-sm text-slate-300 hover:bg-slate-800"
            >
              Close
            </button>
            <button
              type="button"
              @click="showDetails = false; openEdit(selectedArticle!)"
              class="rounded-xl bg-emerald-500 px-4 py-2.5 text-sm font-semibold text-slate-950 hover:bg-emerald-400"
            >
              Edit article
            </button>
          </div>
        </div>
      </article>
    </div>
  </div>
</template>