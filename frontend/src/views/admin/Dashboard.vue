<template>
  <div class="min-h-screen space-y-6 bg-[#070A0F] p-6 text-white">
    <div class="flex flex-wrap items-center justify-between gap-4">
      <div>
        <h1 class="text-2xl font-bold">Admin Dashboard</h1>
        <p class="mt-1 text-sm text-gray-400">
          Football Intelligence Decision System
        </p>
      </div>

      <button
        type="button"
        @click="loadDashboard"
        :disabled="loading"
        class="rounded-lg bg-lime-400 px-4 py-2 font-semibold text-black disabled:opacity-50"
      >
        {{ loading ? 'Loading...' : 'Refresh Data' }}
      </button>
    </div>

    <div
      v-if="error"
      class="rounded-lg border border-red-500/30 bg-red-500/10 p-4 text-red-300"
    >
      <p class="font-semibold">Unable to load dashboard</p>
      <p class="mt-1 text-sm">{{ error }}</p>
      <p class="mt-2 text-xs text-gray-400">
        تأكد من تشغيل Django Backend وتسجيل الدخول بحساب Admin.
      </p>
    </div>

    <div v-if="loading && !hasLoaded" class="py-12 text-center text-gray-400">
      Loading dashboard data...
    </div>

    <template v-else>
      <div class="grid grid-cols-1 gap-4 sm:grid-cols-2 xl:grid-cols-4">
        <div
          v-for="card in statCards"
          :key="card.key"
          class="rounded-xl border border-white/10 bg-[#0F141C] p-5"
        >
          <p class="text-sm text-gray-400">{{ card.label }}</p>
          <p class="mt-3 text-3xl font-bold text-lime-300">
            {{ formatNumber(stats[card.key]) }}
          </p>
          <p class="mt-2 text-xs text-gray-500">Live backend data</p>
        </div>
      </div>

      <div class="grid grid-cols-1 gap-6 xl:grid-cols-2">
        <section class="overflow-hidden rounded-xl border border-white/10 bg-[#0F141C]">
          <div class="border-b border-white/10 p-5">
            <h2 class="text-lg font-semibold">Recent Users</h2>
            <p class="mt-1 text-sm text-gray-400">
              Latest registered accounts
            </p>
          </div>

          <div v-if="recentUsers.length" class="divide-y divide-white/5">
            <div
              v-for="user in recentUsers"
              :key="user.id"
              class="flex items-center justify-between gap-4 p-4"
            >
              <div class="min-w-0">
                <p class="truncate font-medium">
                  {{ user.name || user.username }}
                </p>
                <p class="truncate text-sm text-gray-400">
                  {{ user.email || 'No email provided' }}
                </p>
                <p class="mt-1 text-xs text-gray-500">
                  {{ formatDate(user.date_joined) }}
                </p>
              </div>

              <span
                class="shrink-0 rounded-full px-3 py-1 text-xs"
                :class="user.is_active
                  ? 'bg-lime-400/10 text-lime-300'
                  : 'bg-gray-500/10 text-gray-400'"
              >
                {{ user.is_active ? 'Active' : 'Inactive' }}
              </span>
            </div>
          </div>

          <p v-else class="p-5 text-sm text-gray-400">
            No users found.
          </p>
        </section>

        <section class="overflow-hidden rounded-xl border border-white/10 bg-[#0F141C]">
          <div class="border-b border-white/10 p-5">
            <h2 class="text-lg font-semibold">Recent Analyses</h2>
            <p class="mt-1 text-sm text-gray-400">
              Latest saved football analyses
            </p>
          </div>

          <div v-if="recentAnalyses.length" class="divide-y divide-white/5">
            <article
              v-for="analysis in recentAnalyses"
              :key="analysis.id"
              class="p-4"
            >
              <div class="flex flex-wrap items-start justify-between gap-2">
                <h3 class="font-medium">
                  {{ analysis.title || 'Untitled analysis' }}
                </h3>
                <span class="rounded bg-white/5 px-2 py-1 text-xs text-lime-300">
                  {{ analysis.analysis_type || 'Analysis' }}
                </span>
              </div>

              <p class="mt-2 text-sm text-gray-400">
                {{ analysis.summary || 'No summary available.' }}
              </p>

              <div class="mt-3 flex flex-wrap justify-between gap-2 text-xs text-gray-500">
                <span>By: {{ analysis.created_by || 'Unknown' }}</span>
                <span>{{ formatDate(analysis.created_at) }}</span>
              </div>
            </article>
          </div>

          <p v-else class="p-5 text-sm text-gray-400">
            No saved analyses found.
          </p>
        </section>
      </div>

      <p v-if="generatedAt" class="text-right text-xs text-gray-500">
        Last updated: {{ formatDate(generatedAt) }}
      </p>
    </template>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'

interface DashboardStats {
  total_users: number
  active_users: number
  total_matches: number
  total_analyses: number
  total_teams: number
  total_players: number
  total_competitions: number
}

interface DashboardUser {
  id: number
  username: string
  name: string
  email: string
  role: string
  is_active: boolean
  date_joined: string | null
}

interface DashboardAnalysis {
  id: number
  title: string
  analysis_type: string
  summary: string
  created_at: string | null
  created_by: string | null
}

interface DashboardResponse {
  stats: DashboardStats
  recent_users: DashboardUser[]
  recent_analyses: DashboardAnalysis[]
  generated_at: string
}

const API_BASE_URL = (
  import.meta.env.VITE_API_BASE_URL ||
  'http://127.0.0.1:8000/api/v1'
).replace(/\/+$/, '')

const loading = ref(false)
const hasLoaded = ref(false)
const error = ref('')

const stats = ref<DashboardStats>({
  total_users: 0,
  active_users: 0,
  total_matches: 0,
  total_analyses: 0,
  total_teams: 0,
  total_players: 0,
  total_competitions: 0,
})

const recentUsers = ref<DashboardUser[]>([])
const recentAnalyses = ref<DashboardAnalysis[]>([])
const generatedAt = ref('')

const statCards = computed(() => [
  { key: 'total_users' as const, label: 'Total Users' },
  { key: 'active_users' as const, label: 'Active Users' },
  { key: 'total_matches' as const, label: 'Total Matches' },
  { key: 'total_analyses' as const, label: 'Saved Analyses' },
  { key: 'total_teams' as const, label: 'Teams' },
  { key: 'total_players' as const, label: 'Players' },
  { key: 'total_competitions' as const, label: 'Competitions' },
])

function formatNumber(value: number | undefined): string {
  return new Intl.NumberFormat().format(value ?? 0)
}

function formatDate(value: string | null | undefined): string {
  if (!value) return '—'

  const date = new Date(value)
  if (Number.isNaN(date.getTime())) return value

  return new Intl.DateTimeFormat(undefined, {
    dateStyle: 'medium',
    timeStyle: 'short',
  }).format(date)
}

function getAccessToken(): string | null {
  // Use the same token key saved by Login.vue.
  const tokenKeys = [
    'fids_access_token',
    'access',
    'access_token',
    'accessToken',
    'token',
  ]

  for (const storage of [localStorage, sessionStorage]) {
    for (const key of tokenKeys) {
      const token = storage.getItem(key)
      if (token) return token
    }
  }

  return null
}

async function loadDashboard() {
  if (loading.value) return

  loading.value = true
  error.value = ''

  try {
    const token = getAccessToken()

    if (!token) {
      throw new Error('No access token found. Please sign in again.')
    }

    const response = await fetch(`${API_BASE_URL}/admin/dashboard/`, {
      method: 'GET',
      headers: {
        Accept: 'application/json',
        Authorization: `Bearer ${token}`,
      },
    })

    if (response.status === 401) {
      throw new Error(
        'Authentication failed (401). Sign in again to refresh your access token.',
      )
    }

    if (response.status === 403) {
      throw new Error(
        'Access denied (403). Your account must have Django staff/admin permissions.',
      )
    }

    if (!response.ok) {
      throw new Error(`API request failed (${response.status}).`)
    }

    const data = (await response.json()) as DashboardResponse

    if (!data.stats) {
      throw new Error('The dashboard API response is missing the stats object.')
    }

    stats.value = data.stats
    recentUsers.value = data.recent_users ?? []
    recentAnalyses.value = data.recent_analyses ?? []
    generatedAt.value = data.generated_at ?? ''
    hasLoaded.value = true
  } catch (err) {
    error.value =
      err instanceof TypeError
        ? 'Cannot connect to Django. Check that the backend is running and the API URL is correct.'
        : err instanceof Error
          ? err.message
          : 'An unexpected error occurred while loading the dashboard.'
  } finally {
    loading.value = false
  }
}

onMounted(loadDashboard)
</script>
