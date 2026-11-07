
<template>
  <div class="min-h-screen space-y-6 bg-slate-950 p-4 text-slate-100 sm:p-6 lg:p-8">

    <!-- Header -->
    <header class="flex flex-col justify-between gap-4 sm:flex-row sm:items-center">
      <div>
        <div class="mb-2 flex items-center gap-2 text-xs font-semibold uppercase tracking-[0.2em] text-indigo-400">
          <span>FIDS</span>
          <span class="text-slate-600">/</span>
          <span>Administration</span>
        </div>

        <h1 class="text-3xl font-bold tracking-tight sm:text-4xl">
          Competitions
        </h1>

        <p class="mt-2 text-sm text-slate-400">
          Manage football leagues, cups, seasons, and competition data.
        </p>
      </div>

      <button
        @click="openCreateModal"
        class="rounded-xl bg-indigo-600 px-5 py-3 text-sm font-semibold text-white transition hover:bg-indigo-500"
      >
        + Add Competition
      </button>
    </header>

    <!-- Notifications -->
    <div
      v-if="successMessage"
      class="rounded-xl border border-emerald-500/30 bg-emerald-500/10 p-4 text-sm text-emerald-400"
    >
      {{ successMessage }}
    </div>

    <div
      v-if="errorMessage"
      class="rounded-xl border border-red-500/30 bg-red-500/10 p-4 text-sm text-red-400"
    >
      {{ errorMessage }}
    </div>

    <!-- Statistics -->
    <section class="grid grid-cols-1 gap-4 sm:grid-cols-3">
      <article
        v-for="stat in statCards"
        :key="stat.label"
        class="rounded-2xl border border-slate-800 bg-slate-900 p-5"
      >
        <p class="text-sm text-slate-400">{{ stat.label }}</p>
        <h2 class="mt-3 text-3xl font-bold">{{ stat.value }}</h2>
        <p class="mt-2 text-xs text-slate-500">{{ stat.description }}</p>
      </article>
    </section>

    <!-- Search -->
    <section class="rounded-2xl border border-slate-800 bg-slate-900 p-4">
      <div class="flex flex-col gap-3 sm:flex-row">
        <input
          v-model="searchQuery"
          type="search"
          placeholder="Search competitions, countries, or seasons..."
          class="min-w-0 flex-1 rounded-xl border border-slate-700 bg-slate-950 px-4 py-3 text-sm outline-none focus:border-indigo-500"
        />

        <button
          @click="fetchCompetitions"
          :disabled="loading"
          class="rounded-xl border border-slate-700 px-5 py-3 text-sm text-slate-300 transition hover:bg-slate-800 disabled:opacity-50"
        >
          {{ loading ? 'Loading...' : 'Refresh' }}
        </button>
      </div>

      <p class="mt-3 text-xs text-slate-500">
        {{ filteredCompetitions.length }} competitions found
      </p>
    </section>

    <!-- Table -->
    <section class="overflow-hidden rounded-2xl border border-slate-800 bg-slate-900">
      <div class="flex items-center justify-between border-b border-slate-800 p-5">
        <div>
          <h2 class="text-lg font-semibold">All Competitions</h2>
          <p class="mt-1 text-sm text-slate-400">
            Competition directory
          </p>
        </div>

        <span class="rounded-lg bg-slate-800 px-3 py-2 text-xs text-slate-300">
          {{ filteredCompetitions.length }} records
        </span>
      </div>

      <div class="overflow-x-auto">
        <table class="w-full min-w-[750px] text-left">
          <thead class="bg-slate-950/60">
            <tr>
              <th class="px-5 py-4 text-xs font-semibold uppercase text-slate-400">Competition</th>
              <th class="px-5 py-4 text-xs font-semibold uppercase text-slate-400">Country</th>
              <th class="px-5 py-4 text-xs font-semibold uppercase text-slate-400">Season</th>
              <th class="px-5 py-4 text-xs font-semibold uppercase text-slate-400">Created</th>
              <th class="px-5 py-4 text-right text-xs font-semibold uppercase text-slate-400">Actions</th>
            </tr>
          </thead>

          <tbody>
            <tr
              v-for="competition in filteredCompetitions"
              :key="competition.id"
              class="border-t border-slate-800 transition hover:bg-slate-800/40"
            >
              <!-- Competition -->
              <td class="px-5 py-4">
                <div class="flex items-center gap-3">
                  <div class="flex h-11 w-11 shrink-0 items-center justify-center overflow-hidden rounded-xl border border-slate-700 bg-slate-800">
                    <img
                      v-if="competition.logo"
                      :src="competition.logo"
                      :alt="competition.name"
                      class="h-full w-full object-contain p-1"
                      @error="onLogoError"
                    />
                    <span v-else class="text-xl">🏆</span>
                  </div>

                  <div>
                    <p class="font-medium text-slate-100">
                      {{ competition.name }}
                    </p>
                    <p class="mt-1 text-xs text-slate-500">
                      ID: {{ competition.id }}
                    </p>
                  </div>
                </div>
              </td>

              <td class="px-5 py-4 text-sm text-slate-300">
                {{ competition.country || '—' }}
              </td>

              <td class="px-5 py-4">
                <span class="rounded-lg bg-indigo-500/10 px-3 py-1.5 text-xs text-indigo-300">
                  {{ competition.season || '—' }}
                </span>
              </td>

              <td class="px-5 py-4 text-sm text-slate-400">
                {{ formatDate(competition.created_at) }}
              </td>

              <td class="px-5 py-4">
                <div class="flex justify-end gap-2">
                  <button
                    @click="viewCompetition(competition)"
                    class="rounded-lg border border-slate-700 px-3 py-2 text-xs text-slate-300 transition hover:border-indigo-500 hover:text-indigo-300"
                  >
                    View
                  </button>

                  <button
                    @click="openEditModal(competition)"
                    class="rounded-lg border border-slate-700 px-3 py-2 text-xs text-slate-300 transition hover:border-indigo-500 hover:text-indigo-300"
                  >
                    Edit
                  </button>

                  <button
                    @click="deleteCompetition(competition)"
                    :disabled="deletingId === competition.id"
                    class="rounded-lg border border-red-500/30 px-3 py-2 text-xs text-red-400 transition hover:bg-red-500/10 disabled:opacity-50"
                  >
                    {{ deletingId === competition.id ? 'Deleting...' : 'Delete' }}
                  </button>
                </div>
              </td>
            </tr>

            <tr v-if="loading">
              <td colspan="5" class="px-5 py-16 text-center text-slate-400">
                Loading competitions...
              </td>
            </tr>

            <tr v-else-if="filteredCompetitions.length === 0">
              <td colspan="5" class="px-5 py-16 text-center">
                <div class="text-3xl text-slate-600">🏆</div>
                <p class="mt-3 font-medium text-slate-300">
                  No competitions found
                </p>
                <p class="mt-1 text-sm text-slate-500">
                  Add a competition or change your search.
                </p>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </section>

    <!-- Create / Edit Modal -->
    <div
      v-if="showModal"
      class="fixed inset-0 z-50 flex items-center justify-center overflow-y-auto bg-black/70 p-4 backdrop-blur-sm"
      @click.self="closeModal"
    >
      <section class="my-auto w-full max-w-xl rounded-2xl border border-slate-700 bg-slate-900 shadow-2xl">

        <div class="flex items-center justify-between border-b border-slate-800 p-5">
          <div>
            <h2 class="text-xl font-bold">
              {{ editingId === null ? 'Add Competition' : 'Edit Competition' }}
            </h2>
            <p class="mt-1 text-sm text-slate-400">
              Enter competition information.
            </p>
          </div>

          <button
            @click="closeModal"
            class="text-2xl text-slate-400 hover:text-white"
          >
            ×
          </button>
        </div>

        <form @submit.prevent="saveCompetition" class="space-y-5 p-5">

          <div>
            <label class="mb-2 block text-sm font-medium text-slate-300">
              Competition Name *
            </label>
            <input
              v-model.trim="form.name"
              required
              maxlength="150"
              placeholder="e.g. Premier League"
              class="w-full rounded-xl border border-slate-700 bg-slate-950 px-4 py-3 text-sm outline-none focus:border-indigo-500"
            />
          </div>

          <div>
            <label class="mb-2 block text-sm font-medium text-slate-300">
              Country
            </label>
            <input
              v-model.trim="form.country"
              maxlength="100"
              placeholder="e.g. England"
              class="w-full rounded-xl border border-slate-700 bg-slate-950 px-4 py-3 text-sm outline-none focus:border-indigo-500"
            />
          </div>

          <div>
            <label class="mb-2 block text-sm font-medium text-slate-300">
              Season
            </label>
            <input
              v-model.trim="form.season"
              maxlength="20"
              placeholder="2026/27"
              class="w-full rounded-xl border border-slate-700 bg-slate-950 px-4 py-3 text-sm outline-none focus:border-indigo-500"
            />
          </div>

          <div>
            <label class="mb-2 block text-sm font-medium text-slate-300">
              Competition Logo URL
            </label>
            <input
              v-model.trim="form.logo"
              type="url"
              placeholder="https://example.com/logo.png"
              class="w-full rounded-xl border border-slate-700 bg-slate-950 px-4 py-3 text-sm outline-none focus:border-indigo-500"
            />
          </div>

          <div
            v-if="form.logo"
            class="flex items-center gap-3 rounded-xl border border-slate-800 bg-slate-950 p-3"
          >
            <img
              :src="form.logo"
              alt="Logo preview"
              class="h-12 w-12 rounded-lg object-contain"
            />
            <span class="text-xs text-slate-400">Logo preview</span>
          </div>

          <p v-if="formError" class="text-sm text-red-400">
            {{ formError }}
          </p>

          <div class="flex flex-col-reverse gap-3 border-t border-slate-800 pt-5 sm:flex-row sm:justify-end">
            <button
              type="button"
              @click="closeModal"
              class="rounded-xl border border-slate-700 px-5 py-3 text-sm text-slate-300 hover:bg-slate-800"
            >
              Cancel
            </button>

            <button
              type="submit"
              :disabled="saving"
              class="rounded-xl bg-indigo-600 px-5 py-3 text-sm font-semibold text-white transition hover:bg-indigo-500 disabled:opacity-50"
            >
              {{
                saving
                  ? 'Saving...'
                  : editingId === null
                    ? 'Create Competition'
                    : 'Save Changes'
              }}
            </button>
          </div>
        </form>
      </section>
    </div>

    <!-- View Details Modal -->
    <div
      v-if="viewingCompetition"
      class="fixed inset-0 z-50 flex items-center justify-center bg-black/70 p-4 backdrop-blur-sm"
      @click.self="viewingCompetition = null"
    >
      <section class="w-full max-w-lg rounded-2xl border border-slate-700 bg-slate-900 p-6">

        <div class="flex items-center justify-between">
          <h2 class="text-xl font-bold">Competition Details</h2>

          <button
            @click="viewingCompetition = null"
            class="text-2xl text-slate-400 hover:text-white"
          >
            ×
          </button>
        </div>

        <div class="mt-6 flex items-center gap-4">
          <img
            v-if="viewingCompetition.logo"
            :src="viewingCompetition.logo"
            class="h-16 w-16 rounded-xl bg-slate-800 object-contain p-2"
            alt="Competition logo"
          />
          <div
            v-else
            class="flex h-16 w-16 items-center justify-center rounded-xl bg-slate-800 text-3xl"
          >
            🏆
          </div>

          <div>
            <h3 class="text-lg font-semibold">
              {{ viewingCompetition.name }}
            </h3>
            <p class="text-sm text-slate-400">
              {{ viewingCompetition.country || 'Unknown country' }}
            </p>
          </div>
        </div>

        <div class="mt-6 space-y-4">
          <div
            v-for="detail in [
              { label: 'Competition ID', value: viewingCompetition.id },
              { label: 'Country', value: viewingCompetition.country || '—' },
              { label: 'Season', value: viewingCompetition.season || '—' },
              { label: 'Logo URL', value: viewingCompetition.logo || '—' },
              { label: 'Created', value: formatDate(viewingCompetition.created_at) },
            ]"
            :key="detail.label"
            class="flex items-start justify-between gap-4 border-b border-slate-800 pb-3"
          >
            <span class="text-sm text-slate-400">{{ detail.label }}</span>
            <span class="max-w-[65%] break-all text-right text-sm text-slate-200">
              {{ detail.value }}
            </span>
          </div>
        </div>

        <button
          @click="viewingCompetition = null"
          class="mt-6 w-full rounded-xl bg-slate-800 px-4 py-3 text-sm hover:bg-slate-700"
        >
          Close
        </button>
      </section>
    </div>

    <p class="text-xs text-slate-600">
      FIDS Administration · Football Intelligence Decision System
    </p>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'

interface Competition {
  id: number
  name: string
  country: string
  logo: string
  season: string
  created_at?: string
  updated_at?: string
}

interface CompetitionForm {
  name: string
  country: string
  logo: string
  season: string
}

const API_BASE = (
  import.meta.env.VITE_API_BASE_URL ||
  'http://127.0.0.1:8000/api/v1'
).replace(/\/$/, '')

const API_URL = `${API_BASE}/competitions/`

const competitions = ref<Competition[]>([])
const searchQuery = ref('')

const loading = ref(false)
const saving = ref(false)
const deletingId = ref<number | null>(null)

const showModal = ref(false)
const editingId = ref<number | null>(null)

const viewingCompetition = ref<Competition | null>(null)

const successMessage = ref('')
const errorMessage = ref('')
const formError = ref('')

const emptyForm = (): CompetitionForm => ({
  name: '',
  country: '',
  logo: '',
  season: '2026/27',
})

const form = ref<CompetitionForm>(emptyForm())

// Authentication
function getAuthHeaders(): HeadersInit {
  const token =
    localStorage.getItem('fids_access_token') ||
    localStorage.getItem('token')

  return {
    'Content-Type': 'application/json',
    ...(token ? { Authorization: `Bearer ${token}` } : {}),
  }
}

// API error handling
async function getErrorMessage(response: Response): Promise<string> {
  try {
    const data = await response.json()

    if (typeof data === 'string') return data

    if (data.detail) return data.detail

    return Object.entries(data)
      .map(([field, errors]) => {
        const message = Array.isArray(errors)
          ? errors.join(', ')
          : String(errors)

        return `${field}: ${message}`
      })
      .join(' | ') || `Request failed (${response.status})`
  } catch {
    return `Request failed (${response.status})`
  }
}

// GET competitions
async function fetchCompetitions() {
  loading.value = true
  errorMessage.value = ''

  try {
    const response = await fetch(API_URL, {
      method: 'GET',
      headers: getAuthHeaders(),
    })

    if (!response.ok) {
      throw new Error(await getErrorMessage(response))
    }

    const data = await response.json()

    // Supports both DRF pagination and normal arrays.
    competitions.value = Array.isArray(data)
      ? data
      : Array.isArray(data.results)
        ? data.results
        : []

  } catch (error) {
    errorMessage.value =
      error instanceof Error
        ? error.message
        : 'Unable to load competitions.'
  } finally {
    loading.value = false
  }
}

// Search
const filteredCompetitions = computed(() => {
  const query = searchQuery.value.trim().toLowerCase()

  if (!query) return competitions.value

  return competitions.value.filter((competition) =>
    [
      competition.name,
      competition.country,
      competition.season,
    ].some((value) => (value || '').toLowerCase().includes(query)),
  )
})

// Statistics
const statCards = computed(() => [
  {
    label: 'Total Competitions',
    value: competitions.value.length,
    description: 'Registered competitions',
  },
  {
    label: 'Countries',
    value: new Set(
      competitions.value
        .map((item) => item.country)
        .filter(Boolean),
    ).size,
    description: 'Countries represented',
  },
  {
    label: 'Seasons',
    value: new Set(
      competitions.value
        .map((item) => item.season)
        .filter(Boolean),
    ).size,
    description: 'Available seasons',
  },
])

// Modal
function openCreateModal() {
  editingId.value = null
  form.value = emptyForm()
  formError.value = ''
  showModal.value = true
}

function openEditModal(competition: Competition) {
  editingId.value = competition.id

  form.value = {
    name: competition.name,
    country: competition.country || '',
    logo: competition.logo || '',
    season: competition.season || '',
  }

  formError.value = ''
  showModal.value = true
}

function closeModal() {
  showModal.value = false
  editingId.value = null
  formError.value = ''
}

// CREATE / UPDATE
async function saveCompetition() {
  formError.value = ''
  successMessage.value = ''

  if (!form.value.name.trim()) {
    formError.value = 'Competition name is required.'
    return
  }

  saving.value = true

  try {
    const isEditing = editingId.value !== null

    const url = isEditing
      ? `${API_URL}${editingId.value}/`
      : API_URL

    const response = await fetch(url, {
      method: isEditing ? 'PATCH' : 'POST',
      headers: getAuthHeaders(),
      body: JSON.stringify({
        name: form.value.name,
        country: form.value.country,
        logo: form.value.logo,
        season: form.value.season,
      }),
    })

    if (!response.ok) {
      throw new Error(await getErrorMessage(response))
    }

    successMessage.value = isEditing
      ? 'Competition updated successfully.'
      : 'Competition created successfully.'

    closeModal()
    await fetchCompetitions()

  } catch (error) {
    formError.value =
      error instanceof Error
        ? error.message
        : 'Unable to save competition.'
  } finally {
    saving.value = false
  }
}

// DELETE
async function deleteCompetition(competition: Competition) {
  const confirmed = window.confirm(
    `Are you sure you want to delete "${competition.name}"?`,
  )

  if (!confirmed) return

  deletingId.value = competition.id
  errorMessage.value = ''
  successMessage.value = ''

  try {
    const response = await fetch(
      `${API_URL}${competition.id}/`,
      {
        method: 'DELETE',
        headers: getAuthHeaders(),
      },
    )

    if (!response.ok) {
      throw new Error(await getErrorMessage(response))
    }

    successMessage.value = 'Competition deleted successfully.'

    if (viewingCompetition.value?.id === competition.id) {
      viewingCompetition.value = null
    }

    await fetchCompetitions()

  } catch (error) {
    errorMessage.value =
      error instanceof Error
        ? error.message
        : 'Unable to delete competition.'
  } finally {
    deletingId.value = null
  }
}

// View
function viewCompetition(competition: Competition) {
  viewingCompetition.value = competition
}

// Helpers
function formatDate(date?: string) {
  if (!date) return '—'

  const parsed = new Date(date)

  if (Number.isNaN(parsed.getTime())) return '—'

  return parsed.toLocaleDateString()
}

function onLogoError(event: Event) {
  const image = event.target as HTMLImageElement
  image.style.display = 'none'
}

onMounted(() => {
  fetchCompetitions()
})
</script>
