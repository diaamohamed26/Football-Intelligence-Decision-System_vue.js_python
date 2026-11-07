
<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'

interface Team {
  id: number
  name: string
  short_name: string
  country: string
  logo: string | null
  founded: number | null
  created_at?: string
  updated_at?: string
}

interface TeamForm {
  name: string
  short_name: string
  country: string
  logo: string
  founded: number | null
}

interface PaginatedResponse {
  results: Team[]
  count?: number
  next?: string | null
  previous?: string | null
}

const API_URL = 'http://127.0.0.1:8000/api/v1/teams/'

const teams = ref<Team[]>([])
const loading = ref(false)
const saving = ref(false)

const search = ref('')
const countryFilter = ref('All')
const sortBy = ref('name')
const currentPage = ref(1)
const pageSize = 8

const showForm = ref(false)
const showDetails = ref(false)

const editingTeam = ref<Team | null>(null)
const selectedTeam = ref<Team | null>(null)
const deleteTarget = ref<Team | null>(null)

const errorMessage = ref('')
const successMessage = ref('')

const emptyForm = (): TeamForm => ({
  name: '',
  short_name: '',
  country: '',
  logo: '',
  founded: null,
})

const form = ref<TeamForm>(emptyForm())

// ----------------------------------
// API REQUEST
// ----------------------------------

async function apiRequest<T>(
  endpoint: string,
  options: RequestInit = {},
): Promise<T> {
  const token = localStorage.getItem('fids_access_token')

  const headers = new Headers(options.headers)

  headers.set('Content-Type', 'application/json')

  if (token) {
    headers.set('Authorization', `Bearer ${token}`)
  }

  const response = await fetch(endpoint, {
    ...options,
    headers,
  })

  if (response.status === 401) {
    throw new Error('Authentication expired. Please log in again.')
  }

  if (response.status === 204) {
    return undefined as T
  }

  const data = await response.json().catch(() => null)

  if (!response.ok) {
    if (data && typeof data === 'object') {
      const message = Object.entries(data)
        .map(([key, value]) => {
          const detail = Array.isArray(value)
            ? value.join(', ')
            : String(value)

          return `${key}: ${detail}`
        })
        .join('\n')

      throw new Error(message || 'Something went wrong.')
    }

    throw new Error('Request failed. Please try again.')
  }

  return data as T
}

// ----------------------------------
// FETCH TEAMS
// ----------------------------------

async function fetchTeams() {
  loading.value = true
  errorMessage.value = ''

  try {
    const response = await apiRequest<Team[] | PaginatedResponse>(
      API_URL,
    )

    // Supports both normal DRF lists and paginated responses.
    teams.value = Array.isArray(response)
      ? response
      : response.results ?? []

    if (currentPage.value > totalPages.value) {
      currentPage.value = totalPages.value
    }
  } catch (error) {
    errorMessage.value =
      error instanceof Error ? error.message : 'Failed to load teams.'
  } finally {
    loading.value = false
  }
}

onMounted(fetchTeams)

// ----------------------------------
// COMPUTED DATA
// ----------------------------------

const countries = computed(() => [
  ...new Set(teams.value.map(team => team.country).filter(Boolean)),
].sort())

const activeCount = computed(() => teams.value.length)

const countryCount = computed(() => countries.value.length)

const filteredTeams = computed(() => {
  const query = search.value.trim().toLowerCase()

  return teams.value
    .filter(team => {
      const matchesSearch =
        !query ||
        team.name.toLowerCase().includes(query) ||
        team.short_name.toLowerCase().includes(query) ||
        team.country.toLowerCase().includes(query)

      const matchesCountry =
        countryFilter.value === 'All' ||
        team.country === countryFilter.value

      return matchesSearch && matchesCountry
    })
    .sort((a, b) => {
      if (sortBy.value === 'name') {
        return a.name.localeCompare(b.name)
      }

      if (sortBy.value === 'newest') {
        return b.id - a.id
      }

      if (sortBy.value === 'oldest') {
        return a.id - b.id
      }

      return 0
    })
})

const totalPages = computed(() =>
  Math.max(1, Math.ceil(filteredTeams.value.length / pageSize)),
)

const paginatedTeams = computed(() => {
  const start = (currentPage.value - 1) * pageSize

  return filteredTeams.value.slice(start, start + pageSize)
})

const firstItem = computed(() =>
  filteredTeams.value.length
    ? (currentPage.value - 1) * pageSize + 1
    : 0,
)

const lastItem = computed(() =>
  Math.min(
    currentPage.value * pageSize,
    filteredTeams.value.length,
  ),
)

// ----------------------------------
// CREATE TEAM
// ----------------------------------

function openCreate() {
  editingTeam.value = null
  form.value = emptyForm()
  errorMessage.value = ''
  showForm.value = true
}

async function createTeam() {
  saving.value = true
  errorMessage.value = ''

  try {
    const payload = {
      name: form.value.name.trim(),
      short_name: form.value.short_name.trim().toUpperCase(),
      country: form.value.country.trim(),
      logo: form.value.logo.trim() || null,
      founded: form.value.founded || null,
    }

    await apiRequest<Team>(API_URL, {
      method: 'POST',
      body: JSON.stringify(payload),
    })

    successMessage.value = 'Team created successfully.'
    showForm.value = false
    form.value = emptyForm()

    currentPage.value = 1
    await fetchTeams()
  } catch (error) {
    errorMessage.value =
      error instanceof Error ? error.message : 'Failed to create team.'
  } finally {
    saving.value = false
  }
}

// ----------------------------------
// EDIT TEAM
// ----------------------------------

function openEdit(team: Team) {
  editingTeam.value = team

  form.value = {
    name: team.name,
    short_name: team.short_name,
    country: team.country,
    logo: team.logo ?? '',
    founded: team.founded,
  }

  errorMessage.value = ''
  showDetails.value = false
  showForm.value = true
}

async function updateTeam() {
  if (!editingTeam.value) return

  saving.value = true
  errorMessage.value = ''

  try {
    const payload = {
      name: form.value.name.trim(),
      short_name: form.value.short_name.trim().toUpperCase(),
      country: form.value.country.trim(),
      logo: form.value.logo.trim() || null,
      founded: form.value.founded || null,
    }

    await apiRequest<Team>(
      `${API_URL}${editingTeam.value.id}/`,
      {
        method: 'PATCH',
        body: JSON.stringify(payload),
      },
    )

    successMessage.value = 'Team updated successfully.'
    showForm.value = false

    await fetchTeams()
  } catch (error) {
    errorMessage.value =
      error instanceof Error ? error.message : 'Failed to update team.'
  } finally {
    saving.value = false
  }
}

// ----------------------------------
// SAVE TEAM
// ----------------------------------

async function saveTeam() {
  const name = form.value.name.trim()
  const shortName = form.value.short_name.trim()
  const country = form.value.country.trim()

  if (!name || !shortName || !country) {
    errorMessage.value =
      'Please fill in the team name, short name, and country.'
    return
  }

  if (
    form.value.founded !== null &&
    (
      form.value.founded < 1800 ||
      form.value.founded > new Date().getFullYear()
    )
  ) {
    errorMessage.value = 'Please enter a valid founded year.'
    return
  }

  if (editingTeam.value) {
    await updateTeam()
  } else {
    await createTeam()
  }
}

// ----------------------------------
// DELETE TEAM
// ----------------------------------

function confirmDelete(team: Team) {
  deleteTarget.value = team
}

async function deleteTeam() {
  if (!deleteTarget.value) return

  const team = deleteTarget.value

  saving.value = true
  errorMessage.value = ''

  try {
    await apiRequest<void>(
      `${API_URL}${team.id}/`,
      { method: 'DELETE' },
    )

    successMessage.value = `${team.name} deleted successfully.`
    deleteTarget.value = null

    await fetchTeams()
  } catch (error) {
    errorMessage.value =
      error instanceof Error ? error.message : 'Failed to delete team.'
  } finally {
    saving.value = false
  }
}

// ----------------------------------
// DETAILS
// ----------------------------------

function openDetails(team: Team) {
  selectedTeam.value = team
  showDetails.value = true
}

// ----------------------------------
// FILTERS & PAGINATION
// ----------------------------------

function resetFilters() {
  search.value = ''
  countryFilter.value = 'All'
  sortBy.value = 'name'
  currentPage.value = 1
}

function changePage(page: number) {
  currentPage.value = Math.min(
    Math.max(1, page),
    totalPages.value,
  )
}
</script>



<template>
  <div class="min-h-screen bg-[#090d16] px-4 py-6 text-slate-100 sm:px-6 lg:px-8">
    <div class="mx-auto max-w-7xl space-y-7">

      <!-- HEADER -->
      <header class="flex flex-col justify-between gap-5 sm:flex-row sm:items-center">
        <div>
          <div class="mb-2 flex items-center gap-2 text-xs font-semibold uppercase tracking-[0.22em] text-cyan-400">
            <span class="h-2 w-2 rounded-full bg-cyan-400"></span>
            Football Intelligence System
          </div>

          <h1 class="text-3xl font-bold tracking-tight text-white sm:text-4xl">
            Teams<span class="text-cyan-400">.</span>
          </h1>

          <p class="mt-2 text-sm text-slate-400">
            Manage football clubs, countries and team information.
          </p>
        </div>

        <div class="flex flex-wrap gap-3">
          <button
            type="button"
            @click="fetchTeams"
            :disabled="loading"
            class="rounded-xl border border-slate-700 px-4 py-3 text-sm font-semibold text-slate-300 transition hover:border-cyan-400 hover:text-cyan-300 disabled:opacity-50"
          >
            <span :class="{ 'animate-spin inline-block': loading }">↻</span>
            Refresh
          </button>

          <button
            type="button"
            @click="openCreate"
            class="inline-flex items-center justify-center gap-2 rounded-xl bg-cyan-400 px-5 py-3 text-sm font-bold text-slate-950 transition hover:bg-cyan-300"
          >
            <span class="text-xl">+</span>
            Add team
          </button>
        </div>
      </header>

      <!-- SUCCESS MESSAGE -->
      <div
        v-if="successMessage"
        class="flex items-center justify-between gap-3 rounded-xl border border-emerald-500/30 bg-emerald-500/10 px-4 py-3 text-sm text-emerald-300"
        role="status"
      >
        <span>✓ {{ successMessage }}</span>

        <button
          type="button"
          @click="successMessage = ''"
          aria-label="Dismiss message"
        >
          ✕
        </button>
      </div>

      <!-- ERROR MESSAGE -->
      <div
        v-if="errorMessage && !showForm"
        class="flex items-center justify-between gap-3 rounded-xl border border-rose-500/30 bg-rose-500/10 px-4 py-3 text-sm text-rose-300"
        role="alert"
      >
        <span class="whitespace-pre-line">{{ errorMessage }}</span>
        <button type="button" @click="errorMessage = ''">✕</button>
      </div>

      <!-- STATISTICS -->
      <section class="grid grid-cols-1 gap-4 sm:grid-cols-3">

        <article class="rounded-2xl border border-slate-800 bg-[#0e1420] p-5">
          <div class="flex items-center justify-between">
            <span class="text-sm text-slate-400">Total teams</span>
            <span class="flex h-10 w-10 items-center justify-center rounded-xl bg-cyan-400/10 text-xl text-cyan-300">
              ⚽
            </span>
          </div>
          <p class="mt-4 text-3xl font-bold text-white">
            {{ teams.length }}
          </p>
          <p class="mt-2 text-xs text-slate-500">
            Records from Django database
          </p>
        </article>

        <article class="rounded-2xl border border-slate-800 bg-[#0e1420] p-5">
          <div class="flex items-center justify-between">
            <span class="text-sm text-slate-400">Countries</span>
            <span class="flex h-10 w-10 items-center justify-center rounded-xl bg-violet-400/10 text-xl text-violet-300">
              ◎
            </span>
          </div>
          <p class="mt-4 text-3xl font-bold text-white">
            {{ countryCount }}
          </p>
          <p class="mt-2 text-xs text-slate-500">
            Countries represented
          </p>
        </article>

        <article class="rounded-2xl border border-slate-800 bg-[#0e1420] p-5">
          <div class="flex items-center justify-between">
            <span class="text-sm text-slate-400">Search results</span>
            <span class="flex h-10 w-10 items-center justify-center rounded-xl bg-emerald-400/10 text-xl text-emerald-300">
              ⌕
            </span>
          </div>
          <p class="mt-4 text-3xl font-bold text-white">
            {{ filteredTeams.length }}
          </p>
          <p class="mt-2 text-xs text-slate-500">
            Matching teams
          </p>
        </article>

      </section>

      <!-- TEAM DIRECTORY -->
      <section class="overflow-hidden rounded-2xl border border-slate-800 bg-[#0e1420]">

        <!-- TABLE HEADER -->
        <div class="flex flex-col justify-between gap-4 border-b border-slate-800 p-5 lg:flex-row lg:items-center">
          <div>
            <h2 class="text-lg font-bold text-white">Club directory</h2>
            <p class="mt-1 text-xs text-slate-500">
              Search, view, create, edit and delete teams.
            </p>
          </div>

          <!-- SEARCH & FILTERS -->
          <div class="grid grid-cols-1 gap-3 sm:grid-cols-3">

            <label class="relative">
              <span class="sr-only">Search teams</span>
              <span class="absolute left-3 top-1/2 -translate-y-1/2 text-slate-500">
                ⌕
              </span>
              <input
                v-model="search"
                type="search"
                placeholder="Search teams..."
                @input="currentPage = 1"
                class="w-full rounded-xl border border-slate-700 bg-[#090d16] py-3 pl-9 pr-3 text-sm text-white outline-none placeholder:text-slate-600 focus:border-cyan-400"
              />
            </label>

            <select
              v-model="countryFilter"
              @change="currentPage = 1"
              class="rounded-xl border border-slate-700 bg-[#090d16] px-3 py-3 text-sm text-slate-300 outline-none focus:border-cyan-400"
            >
              <option value="All">All countries</option>
              <option
                v-for="country in countries"
                :key="country"
                :value="country"
              >
                {{ country }}
              </option>
            </select>

            <select
              v-model="sortBy"
              class="rounded-xl border border-slate-700 bg-[#090d16] px-3 py-3 text-sm text-slate-300 outline-none focus:border-cyan-400"
            >
              <option value="name">Sort: Name</option>
              <option value="newest">Sort: Newest</option>
              <option value="oldest">Sort: Oldest</option>
            </select>

          </div>
        </div>

        <!-- TABLE INFORMATION -->
        <div class="flex flex-wrap items-center justify-between gap-3 px-5 py-4">
          <p class="text-sm text-slate-400">
            Showing
            <span class="font-semibold text-white">{{ firstItem }}–{{ lastItem }}</span>
            of
            <span class="font-semibold text-white">{{ filteredTeams.length }}</span>
            teams
          </p>

          <button
            type="button"
            @click="resetFilters"
            class="text-xs font-semibold text-cyan-300 hover:text-cyan-200"
          >
            Reset filters
          </button>
        </div>

        <!-- TABLE -->
        <div class="overflow-x-auto">
          <table class="w-full min-w-[850px] text-left">

            <thead class="border-y border-slate-800 bg-[#090d16]/70">
              <tr class="text-[11px] font-semibold uppercase tracking-wider text-slate-500">
                <th class="px-5 py-4">Team</th>
                <th class="px-5 py-4">Short name</th>
                <th class="px-5 py-4">Country</th>
                <th class="px-5 py-4">Founded</th>
                <th class="px-5 py-4">Created</th>
                <th class="px-5 py-4 text-right">Actions</th>
              </tr>
            </thead>

            <tbody class="divide-y divide-slate-800/80">

              <tr
                v-for="team in paginatedTeams"
                :key="team.id"
                class="transition hover:bg-slate-800/25"
              >

                <!-- TEAM -->
                <td class="px-5 py-4">
                  <button
                    type="button"
                    class="flex items-center gap-3 text-left"
                    @click="openDetails(team)"
                  >
                    <img
                      v-if="team.logo"
                      :src="team.logo"
                      :alt="team.name"
                      class="h-11 w-11 rounded-xl border border-slate-700 bg-slate-900 object-contain"
                    />

                    <span
                      v-else
                      class="flex h-11 w-11 shrink-0 items-center justify-center rounded-xl border border-cyan-400/20 bg-cyan-400/10 text-xs font-black text-cyan-300"
                    >
                      {{ team.short_name }}
                    </span>

                    <span>
                      <span class="block font-semibold text-white hover:text-cyan-300">
                        {{ team.name }}
                      </span>
                      <span class="mt-1 block text-xs text-slate-500">
                        Team #{{ team.id }}
                      </span>
                    </span>
                  </button>
                </td>

                <!-- SHORT NAME -->
                <td class="px-5 py-4">
                  <span class="rounded-lg bg-slate-800 px-3 py-1.5 text-xs font-bold text-cyan-300">
                    {{ team.short_name }}
                  </span>
                </td>

                <!-- COUNTRY -->
                <td class="px-5 py-4 text-sm text-slate-300">
                  {{ team.country }}
                </td>

                <!-- FOUNDED -->
                <td class="px-5 py-4 text-sm text-slate-300">
                  {{ team.founded ?? '—' }}
                </td>

                <!-- CREATED -->
                <td class="px-5 py-4 text-sm text-slate-400">
                  {{
                    team.created_at
                      ? new Date(team.created_at).toLocaleDateString()
                      : '—'
                  }}
                </td>

                <!-- ACTIONS -->
                <td class="px-5 py-4">
                  <div class="flex justify-end gap-1">

                    <button
                      type="button"
                      title="View team"
                      aria-label="View team"
                      class="rounded-lg p-2 text-slate-400 transition hover:bg-slate-700 hover:text-cyan-300"
                      @click="openDetails(team)"
                    >
                      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" class="h-4 w-4">
                        <path d="M2 12s3.6-7 10-7 10 7 10 7-3.6 7-10 7S2 12 2 12Z"/>
                        <circle cx="12" cy="12" r="3"/>
                      </svg>
                    </button>

                    <button
                      type="button"
                      title="Edit team"
                      aria-label="Edit team"
                      class="rounded-lg p-2 text-slate-400 transition hover:bg-slate-700 hover:text-cyan-300"
                      @click="openEdit(team)"
                    >
                      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" class="h-4 w-4">
                        <path d="m14 6 4 4M4 20l4.5-1 11-11a2.1 2.1 0 0 0-3-3l-11 11L4 20Z"/>
                      </svg>
                    </button>

                    <button
                      type="button"
                      title="Delete team"
                      aria-label="Delete team"
                      class="rounded-lg p-2 text-slate-400 transition hover:bg-rose-500/10 hover:text-rose-300"
                      @click="confirmDelete(team)"
                    >
                      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" class="h-4 w-4">
                        <path d="M3 6h18M8 6V4h8v2m3 0-1 14H6L5 6m4 4v6m6-6v6"/>
                      </svg>
                    </button>

                  </div>
                </td>
              </tr>

              <!-- LOADING -->
              <tr v-if="loading">
                <td colspan="6" class="px-5 py-16 text-center">
                  <div class="mx-auto h-8 w-8 animate-spin rounded-full border-2 border-cyan-400 border-t-transparent"></div>
                  <p class="mt-4 text-sm text-slate-400">
                    Loading teams from Django...
                  </p>
                </td>
              </tr>

              <!-- EMPTY -->
              <tr v-else-if="paginatedTeams.length === 0">
                <td colspan="6" class="px-5 py-16 text-center">
                  <div class="mx-auto flex h-14 w-14 items-center justify-center rounded-2xl bg-slate-800 text-2xl">
                    ⚽
                  </div>
                  <p class="mt-4 font-semibold text-white">
                    No teams found
                  </p>
                  <p class="mt-1 text-sm text-slate-500">
                    Create a team or change your filters.
                  </p>
                  <button
                    type="button"
                    @click="resetFilters"
                    class="mt-4 text-sm font-semibold text-cyan-300"
                  >
                    Clear filters
                  </button>
                </td>
              </tr>

            </tbody>
          </table>
        </div>

        <!-- PAGINATION -->
        <div class="flex flex-col justify-between gap-4 border-t border-slate-800 px-5 py-4 sm:flex-row sm:items-center">
          <p class="text-xs text-slate-500">
            Page {{ currentPage }} of {{ totalPages }}
          </p>

          <div class="flex flex-wrap items-center gap-2">

            <button
              type="button"
              :disabled="currentPage === 1"
              @click="changePage(currentPage - 1)"
              class="rounded-lg border border-slate-700 px-3 py-2 text-sm text-slate-300 hover:border-cyan-400 disabled:cursor-not-allowed disabled:opacity-40"
            >
              Previous
            </button>

            <button
              v-for="page in totalPages"
              :key="page"
              type="button"
              @click="changePage(page)"
              :class="currentPage === page
                ? 'bg-cyan-400 text-slate-950'
                : 'border border-slate-700 text-slate-400 hover:text-white'"
              class="h-9 min-w-9 rounded-lg px-3 text-sm font-semibold"
            >
              {{ page }}
            </button>

            <button
              type="button"
              :disabled="currentPage === totalPages"
              @click="changePage(currentPage + 1)"
              class="rounded-lg border border-slate-700 px-3 py-2 text-sm text-slate-300 hover:border-cyan-400 disabled:cursor-not-allowed disabled:opacity-40"
            >
              Next
            </button>

          </div>
        </div>

      </section>

      <!-- API INFORMATION -->
      <div class="flex flex-wrap items-center justify-between gap-3 text-xs text-slate-500">
        <p>
          FIDS · Football Intelligence Decision System
        </p>
        <p class="flex items-center gap-2">
          <span class="h-2 w-2 rounded-full bg-emerald-400"></span>
          Django REST API integration
        </p>
      </div>

    </div>

    <!-- ================================= -->
    <!-- CREATE / EDIT TEAM MODAL -->
    <!-- ================================= -->

    <Teleport to="body">
      <div
        v-if="showForm"
        class="fixed inset-0 z-50 flex items-center justify-center overflow-y-auto bg-black/75 p-4 backdrop-blur-sm"
        @click.self="showForm = false"
        @keydown.esc="showForm = false"
      >
        <section
          role="dialog"
          aria-modal="true"
          :aria-label="editingTeam ? 'Edit team' : 'Add team'"
          class="my-auto max-h-[92vh] w-full max-w-2xl overflow-y-auto rounded-2xl border border-slate-700 bg-[#0e1420] shadow-2xl"
        >

          <header class="flex items-center justify-between border-b border-slate-800 px-6 py-5">
            <div>
              <h2 class="text-lg font-bold text-white">
                {{ editingTeam ? 'Edit team' : 'Add new team' }}
              </h2>
              <p class="mt-1 text-xs text-slate-500">
                Enter the club information below.
              </p>
            </div>

            <button
              type="button"
              @click="showForm = false"
              class="rounded-lg p-2 text-slate-400 hover:bg-slate-800 hover:text-white"
            >
              ✕
            </button>
          </header>

          <form class="space-y-5 p-6" @submit.prevent="saveTeam">

            <div
              v-if="errorMessage"
              class="whitespace-pre-line rounded-xl border border-rose-500/30 bg-rose-500/10 px-4 py-3 text-sm text-rose-300"
              role="alert"
            >
              {{ errorMessage }}
            </div>

            <div class="grid grid-cols-1 gap-5 sm:grid-cols-2">

              <label class="block sm:col-span-2">
                <span class="mb-2 block text-sm text-slate-300">
                  Team name *
                </span>
                <input
                  v-model="form.name"
                  required
                  maxlength="100"
                  placeholder="e.g. Manchester City"
                  class="w-full rounded-xl border border-slate-700 bg-[#090d16] px-4 py-3 text-sm text-white outline-none focus:border-cyan-400"
                />
              </label>

              <label class="block">
                <span class="mb-2 block text-sm text-slate-300">
                  Short name *
                </span>
                <input
                  v-model="form.short_name"
                  required
                  maxlength="10"
                  placeholder="e.g. MCI"
                  class="w-full rounded-xl border border-slate-700 bg-[#090d16] px-4 py-3 text-sm uppercase text-white outline-none focus:border-cyan-400"
                />
              </label>

              <label class="block">
                <span class="mb-2 block text-sm text-slate-300">
                  Country *
                </span>
                <input
                  v-model="form.country"
                  required
                  maxlength="100"
                  placeholder="e.g. England"
                  class="w-full rounded-xl border border-slate-700 bg-[#090d16] px-4 py-3 text-sm text-white outline-none focus:border-cyan-400"
                />
              </label>

              <label class="block sm:col-span-2">
                <span class="mb-2 block text-sm text-slate-300">
                  Team logo URL
                </span>
                <input
                  v-model="form.logo"
                  type="url"
                  placeholder="https://example.com/logo.png"
                  class="w-full rounded-xl border border-slate-700 bg-[#090d16] px-4 py-3 text-sm text-white outline-none focus:border-cyan-400"
                />
              </label>

              <label class="block">
                <span class="mb-2 block text-sm text-slate-300">
                  Founded year
                </span>
                <input
                  v-model.number="form.founded"
                  type="number"
                  min="1800"
                  :max="new Date().getFullYear()"
                  placeholder="e.g. 1880"
                  class="w-full rounded-xl border border-slate-700 bg-[#090d16] px-4 py-3 text-sm text-white outline-none focus:border-cyan-400"
                />
              </label>

            </div>

            <footer class="flex flex-col-reverse gap-3 border-t border-slate-800 pt-5 sm:flex-row sm:justify-end">

              <button
                type="button"
                @click="showForm = false"
                :disabled="saving"
                class="rounded-xl border border-slate-700 px-5 py-3 text-sm font-semibold text-slate-300 hover:bg-slate-800"
              >
                Cancel
              </button>

              <button
                type="submit"
                :disabled="saving"
                class="rounded-xl bg-cyan-400 px-5 py-3 text-sm font-bold text-slate-950 transition hover:bg-cyan-300 disabled:cursor-not-allowed disabled:opacity-50"
              >
                {{
                  saving
                    ? 'Saving...'
                    : editingTeam
                      ? 'Save changes'
                      : 'Create team'
                }}
              </button>

            </footer>
          </form>

        </section>
      </div>
    </Teleport>

    <!-- ================================= -->
    <!-- TEAM DETAILS MODAL -->
    <!-- ================================= -->

    <Teleport to="body">
      <div
        v-if="showDetails && selectedTeam"
        class="fixed inset-0 z-50 flex items-center justify-center bg-black/75 p-4 backdrop-blur-sm"
        @click.self="showDetails = false"
      >
        <section class="w-full max-w-lg overflow-hidden rounded-2xl border border-slate-700 bg-[#0e1420] shadow-2xl">

          <div class="h-1.5 bg-cyan-400"></div>

          <header class="flex items-start justify-between p-6">
            <div class="flex items-center gap-4">

              <img
                v-if="selectedTeam.logo"
                :src="selectedTeam.logo"
                :alt="selectedTeam.name"
                class="h-16 w-16 rounded-2xl bg-slate-900 object-contain"
              />

              <span
                v-else
                class="flex h-16 w-16 items-center justify-center rounded-2xl border border-cyan-400/20 bg-cyan-400/10 text-lg font-black text-cyan-300"
              >
                {{ selectedTeam.short_name }}
              </span>

              <div>
                <h2 class="text-xl font-bold text-white">
                  {{ selectedTeam.name }}
                </h2>
                <p class="mt-1 text-sm text-slate-400">
                  {{ selectedTeam.country }}
                </p>
                <span class="mt-2 inline-flex rounded-full bg-emerald-400/10 px-2.5 py-1 text-xs font-semibold text-emerald-300">
                  Team registered
                </span>
              </div>
            </div>

            <button
              type="button"
              @click="showDetails = false"
              class="rounded-lg p-2 text-slate-400 hover:bg-slate-800 hover:text-white"
            >
              ✕
            </button>
          </header>

          <div class="grid grid-cols-2 gap-3 px-6 pb-6">

            <div class="rounded-xl border border-slate-800 bg-[#090d16] p-4">
              <p class="text-xs text-slate-500">Team ID</p>
              <p class="mt-2 text-2xl font-bold text-white">
                #{{ selectedTeam.id }}
              </p>
            </div>

            <div class="rounded-xl border border-slate-800 bg-[#090d16] p-4">
              <p class="text-xs text-slate-500">Founded</p>
              <p class="mt-2 text-2xl font-bold text-white">
                {{ selectedTeam.founded ?? '—' }}
              </p>
            </div>

            <div class="col-span-2 rounded-xl border border-slate-800 bg-[#090d16] p-4">
              <p class="text-xs text-slate-500">Short name</p>
              <p class="mt-2 text-sm font-semibold text-cyan-300">
                {{ selectedTeam.short_name }}
              </p>
            </div>

            <div class="col-span-2 rounded-xl border border-slate-800 bg-[#090d16] p-4">
              <p class="text-xs text-slate-500">Country</p>
              <p class="mt-2 text-sm font-semibold text-white">
                {{ selectedTeam.country }}
              </p>
            </div>

          </div>

          <footer class="flex justify-end gap-3 border-t border-slate-800 p-5">

            <button
              type="button"
              @click="showDetails = false"
              class="rounded-xl border border-slate-700 px-4 py-2.5 text-sm font-semibold text-slate-300 hover:bg-slate-800"
            >
              Close
            </button>

            <button
              type="button"
              @click="openEdit(selectedTeam!)"
              class="rounded-xl bg-cyan-400 px-4 py-2.5 text-sm font-bold text-slate-950 hover:bg-cyan-300"
            >
              Edit team
            </button>

          </footer>

        </section>
      </div>
    </Teleport>

    <!-- ================================= -->
    <!-- DELETE CONFIRMATION -->
    <!-- ================================= -->

    <Teleport to="body">
      <div
        v-if="deleteTarget"
        class="fixed inset-0 z-[60] flex items-center justify-center bg-black/75 p-4 backdrop-blur-sm"
        @click.self="deleteTarget = null"
      >
        <section
          role="alertdialog"
          aria-modal="true"
          class="w-full max-w-md rounded-2xl border border-slate-700 bg-[#0e1420] p-6 shadow-2xl"
        >

          <div class="flex h-12 w-12 items-center justify-center rounded-xl bg-rose-400/10 text-xl text-rose-300">
            !
          </div>

          <h2 class="mt-4 text-lg font-bold text-white">
            Delete {{ deleteTarget.name }}?
          </h2>

          <p class="mt-2 text-sm leading-6 text-slate-400">
            This action will permanently delete this team from the database.
            Are you sure you want to continue?
          </p>

          <div class="mt-6 flex justify-end gap-3">

            <button
              type="button"
              :disabled="saving"
              @click="deleteTarget = null"
              class="rounded-xl border border-slate-700 px-4 py-2.5 text-sm font-semibold text-slate-300 hover:bg-slate-800"
            >
              Cancel
            </button>

            <button
              type="button"
              :disabled="saving"
              @click="deleteTeam"
              class="rounded-xl bg-rose-500 px-4 py-2.5 text-sm font-bold text-white hover:bg-rose-400 disabled:opacity-50"
            >
              {{ saving ? 'Deleting...' : 'Delete team' }}
            </button>

          </div>

        </section>
      </div>
    </Teleport>

  </div>
</template>

