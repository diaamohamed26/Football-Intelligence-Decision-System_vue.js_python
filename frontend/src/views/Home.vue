
<template>
  <div class="min-h-screen bg-[#070A0F] text-white">

    <!-- Hero -->
    <section class="relative overflow-hidden border-b border-[#202936]">
      <div class="absolute -right-40 -top-40 h-96 w-96 rounded-full bg-[#B7FF3C]/5 blur-3xl"></div>

      <div class="relative mx-auto max-w-7xl px-4 py-24 sm:py-32">
        <div class="max-w-4xl">

          <div class="mb-6 inline-flex items-center gap-2 rounded-full border border-[#B7FF3C]/20 bg-[#B7FF3C]/5 px-4 py-2">
            <span class="h-2 w-2 animate-pulse rounded-full bg-[#B7FF3C]"></span>
            <span class="text-xs font-semibold uppercase tracking-[0.2em] text-[#B7FF3C]">
              Football Intelligence Decision System
            </span>
          </div>

          <h1 class="text-5xl font-black leading-tight sm:text-7xl lg:text-8xl">
            Football Data.
            <span class="block text-[#B7FF3C]">Intelligence.</span>
            <span class="block">Decisions.</span>
          </h1>

          <p class="mt-8 max-w-2xl text-lg leading-8 text-[#8993A4]">
            Transform football data into intelligent decisions.
            Analyze matches, players and teams with powerful
            football intelligence and AI.
          </p>

          <div class="mt-10 flex flex-wrap gap-4">
            <RouterLink
              to="/matches"
              class="rounded-xl bg-[#B7FF3C] px-7 py-4 font-bold text-[#070A0F] transition hover:scale-105"
            >
              Explore Matches →
            </RouterLink>

            <RouterLink
              to="/ai"
              class="rounded-xl border border-[#303B4B] bg-[#0F141C] px-7 py-4 font-semibold transition hover:border-[#B7FF3C] hover:text-[#B7FF3C]"
            >
              Ask FIDS AI
            </RouterLink>
          </div>

        </div>
      </div>
    </section>

    <!-- Backend Statistics -->
    <section class="mx-auto max-w-7xl px-4 py-16">

      <div class="mb-8 flex flex-wrap items-center justify-between gap-4">
        <div>
          <p class="text-xs font-bold uppercase tracking-[0.25em] text-[#B7FF3C]">
            Live Backend Statistics
          </p>

          <h2 class="mt-2 text-3xl font-bold">
            Platform Overview
          </h2>

          <p class="mt-2 text-sm text-[#8993A4]">
            Real data retrieved from Django REST API.
          </p>
        </div>

        <button
          @click="loadStats"
          :disabled="loading"
          class="rounded-xl border border-[#303B4B] bg-[#0F141C] px-5 py-3 text-sm font-semibold transition hover:border-[#B7FF3C] disabled:opacity-50"
        >
          {{ loading ? 'Refreshing...' : '↻ Refresh Data' }}
        </button>
      </div>

      <!-- Loading -->
      <div
        v-if="loading"
        class="grid gap-4 sm:grid-cols-2 lg:grid-cols-4"
      >
        <div
          v-for="n in 4"
          :key="n"
          class="h-36 animate-pulse rounded-2xl border border-[#202936] bg-[#0F141C]"
        ></div>
      </div>

      <!-- Statistics -->
      <div
        v-else
        class="grid gap-4 sm:grid-cols-2 lg:grid-cols-4"
      >
        <div
          v-for="stat in stats"
          :key="stat.label"
          class="rounded-2xl border border-[#202936] bg-[#0F141C] p-6 transition hover:-translate-y-1 hover:border-[#B7FF3C]/50"
        >
          <div class="flex items-center justify-between">
            <span class="text-3xl">{{ stat.icon }}</span>

            <span class="text-xs font-semibold text-[#B7FF3C]">
              LIVE API
            </span>
          </div>

          <p class="mt-5 text-3xl font-black">
            {{ formatNumber(stat.value) }}
          </p>

          <p class="mt-2 text-sm text-[#8993A4]">
            {{ stat.label }}
          </p>
        </div>
      </div>

      <!-- API Error -->
      <div
        v-if="apiErrors.length"
        class="mt-6 rounded-xl border border-red-500/20 bg-red-500/5 p-5"
      >
        <p class="font-semibold text-red-400">
          Some API requests failed
        </p>

        <ul class="mt-2 space-y-1 text-sm text-[#8993A4]">
          <li v-for="error in apiErrors" :key="error">
            {{ error }}
          </li>
        </ul>

        <p class="mt-3 text-xs text-[#8993A4]">
          Check your Django server, API routes and authentication token.
        </p>
      </div>

    </section>

    <!-- Features -->
    <section class="border-y border-[#202936] bg-[#0A0E14]">
      <div class="mx-auto max-w-7xl px-4 py-20">

        <div class="mb-12 max-w-2xl">
          <p class="text-xs font-bold uppercase tracking-[0.25em] text-[#B7FF3C]">
            Explore FIDS
          </p>

          <h2 class="mt-3 text-3xl font-bold sm:text-4xl">
            Football Intelligence Platform
          </h2>

          <p class="mt-4 leading-7 text-[#8993A4]">
            Explore football data and discover insights
            through advanced analytical tools.
          </p>
        </div>

        <div class="grid gap-5 md:grid-cols-2 lg:grid-cols-3">

          <RouterLink
            v-for="feature in features"
            :key="feature.title"
            :to="feature.link"
            class="group rounded-2xl border border-[#202936] bg-[#0F141C] p-7 transition hover:-translate-y-1 hover:border-[#B7FF3C]/50"
          >
            <div class="mb-6 flex h-14 w-14 items-center justify-center rounded-xl bg-[#B7FF3C]/10 text-3xl">
              {{ feature.icon }}
            </div>

            <h3 class="text-xl font-bold transition group-hover:text-[#B7FF3C]">
              {{ feature.title }}
            </h3>

            <p class="mt-3 text-sm leading-7 text-[#8993A4]">
              {{ feature.description }}
            </p>

            <div class="mt-6 text-sm font-bold text-[#B7FF3C]">
              Explore More →
            </div>
          </RouterLink>

        </div>
      </div>
    </section>

    <!-- AI CTA -->
    <section class="mx-auto max-w-7xl px-4 py-20">
      <div class="rounded-3xl border border-[#B7FF3C]/20 bg-[#0F141C] p-8 sm:p-14">
        <p class="text-xs font-bold uppercase tracking-[0.25em] text-[#B7FF3C]">
          Artificial Intelligence
        </p>

        <h2 class="mt-4 text-3xl font-black sm:text-5xl">
          Think Beyond the Score.
        </h2>

        <p class="mt-5 max-w-2xl leading-8 text-[#8993A4]">
          Discover football insights and explore intelligent
          analysis with FIDS AI.
        </p>

        <RouterLink
          to="/ai"
          class="mt-8 inline-flex rounded-xl bg-[#B7FF3C] px-7 py-4 font-bold text-[#070A0F] transition hover:scale-105"
        >
          Discover FIDS AI →
        </RouterLink>
      </div>
    </section>

    <!-- Footer -->
    <footer class="border-t border-[#202936] px-4 py-8">
      <div class="mx-auto flex max-w-7xl flex-col items-center justify-between gap-4 text-sm text-[#8993A4] sm:flex-row">
        <p>
          <span class="font-black text-white">FIDS</span>
          — Football Intelligence Decision System
        </p>

        <p>© {{ new Date().getFullYear() }} FIDS. All rights reserved.</p>
      </div>
    </footer>

  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import axios from 'axios'

// Django API configuration
const API_BASE =
  import.meta.env.VITE_API_BASE_URL ||
  'http://127.0.0.1:8000/api/v1'

const loading = ref(true)
const apiErrors = ref<string[]>([])

// Real backend statistics
const stats = ref([
  { label: 'Matches Tracked', value: 0, icon: '⚽' },
  { label: 'Players', value: 0, icon: '👤' },
  { label: 'Teams', value: 0, icon: '🛡️' },
  { label: 'Competitions', value: 0, icon: '🏆' },
])

// Feature navigation
const features = [
  {
    title: 'Match Analysis',
    description: 'Explore match results, statistics and performance data.',
    icon: '⚽',
    link: '/matches',
  },
  {
    title: 'Player Intelligence',
    description: 'Discover player statistics and individual performance.',
    icon: '👤',
    link: '/players',
  },
  {
    title: 'Team Analysis',
    description: 'Evaluate teams and compare their performance.',
    icon: '🛡️',
    link: '/teams',
  },
  {
    title: 'Competitions',
    description: 'Explore football leagues, seasons and tournaments.',
    icon: '🏆',
    link: '/competitions',
  },
  {
    title: 'AI Intelligence',
    description: 'Explore football questions and AI-powered insights.',
    icon: '🤖',
    link: '/ai',
  },
  {
    title: 'Advanced Analytics',
    description: 'Transform football statistics into useful insights.',
    icon: '📊',
    link: '/analytics',
  },
]

// Read token from login
function getAuthHeaders() {
  const token =
    localStorage.getItem('fids_access_token') ||
    localStorage.getItem('token')

  return token
    ? { Authorization: `Bearer ${token}` }
    : {}
}

// Support Django REST Framework response formats
function extractCount(data: any): number {
  if (Array.isArray(data)) {
    return data.length
  }

  if (typeof data?.count === 'number') {
    return data.count
  }

  if (Array.isArray(data?.results)) {
    return data.results.length
  }

  return 0
}

// Request one endpoint
async function fetchCount(endpoint: string): Promise<number> {
  const response = await axios.get(
    `${API_BASE}/${endpoint}/`,
    {
      headers: getAuthHeaders(),
    },
  )

  return extractCount(response.data)
}

// Load all statistics from Django
async function loadStats() {
  loading.value = true
  apiErrors.value = []

  const endpoints = [
    'matches',
    'players',
    'teams',
    'competitions',
  ]

  const results = await Promise.allSettled(
    endpoints.map(endpoint => fetchCount(endpoint)),
  )

  results.forEach((result, index) => {
    if (result.status === 'fulfilled') {
      stats.value[index].value = result.value
    } else {
      apiErrors.value.push(
        `${endpoints[index]}: ${
          axios.isAxiosError(result.reason)
            ? result.reason.response?.status === 401
              ? 'Authentication required. Please login.'
              : result.reason.message
            : 'Unable to retrieve data.'
        }`,
      )
    }
  })

  loading.value = false
}

// Format numbers
function formatNumber(value: number): string {
  return new Intl.NumberFormat('en-US').format(value)
}

// Load when Home page opens
onMounted(() => {
  loadStats()
})
</script>
