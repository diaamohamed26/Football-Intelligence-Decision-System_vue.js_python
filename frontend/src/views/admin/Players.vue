
<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'

type PlayerStatus = 'Active' | 'Injured' | 'Inactive'
type Position = 'Goalkeeper' | 'Defender' | 'Midfielder' | 'Forward'

interface Player {
  id: number
  name: string
  nationality: string
  team: string
  position: Position
  age: number
  number: number
  appearances: number
  goals: number
  assists: number
  marketValue: number
  status: PlayerStatus
  photo: string
}

interface PlayerForm {
  name: string
  nationality: string
  team: string
  position: Position
  age: number
  number: number
  appearances: number
  goals: number
  assists: number
  marketValue: number
  status: PlayerStatus
  photo: string
}

interface ApiPlayer {
  id: number
  name?: string
  nationality?: string
  team?: string | { id?: number; name?: string }
  position?: Position
  age?: number
  number?: number
  appearances?: number
  goals?: number
  assists?: number
  market_value?: number
  marketValue?: number
  status?: PlayerStatus
  photo?: string
  image?: string
}

interface PaginatedResponse<T> {
  results: T[]
  count?: number
  next?: string | null
  previous?: string | null
}

const API_URL = 'http://127.0.0.1:8000/api/v1/players/'

const positions: Position[] = [
  'Goalkeeper',
  'Defender',
  'Midfielder',
  'Forward',
]

const players = ref<Player[]>([])

const loading = ref(false)
const saving = ref(false)
const errorMessage = ref('')
const successMessage = ref('')

const search = ref('')
const positionFilter = ref<'All' | Position>('All')
const statusFilter = ref<'All' | PlayerStatus>('All')
const teamFilter = ref('All')
const sortBy = ref<'goals' | 'name' | 'value'>('goals')

const showEditor = ref(false)
const showDetails = ref(false)
const editingId = ref<number | null>(null)
const selectedPlayer = ref<Player | null>(null)
const formError = ref('')

const emptyForm = (): PlayerForm => ({
  name: '',
  nationality: '',
  team: '',
  position: 'Midfielder',
  age: 20,
  number: 0,
  appearances: 0,
  goals: 0,
  assists: 0,
  marketValue: 0,
  status: 'Active',
  photo: '',
})

const form = ref<PlayerForm>(emptyForm())

const teams = computed(() =>
  [...new Set(players.value.map(p => p.team).filter(Boolean))].sort(),
)

const activeCount = computed(
  () => players.value.filter(p => p.status === 'Active').length,
)

const injuredCount = computed(
  () => players.value.filter(p => p.status === 'Injured').length,
)

const totalGoals = computed(
  () => players.value.reduce((sum, p) => sum + p.goals, 0),
)

const totalAssists = computed(
  () => players.value.reduce((sum, p) => sum + p.assists, 0),
)

const totalMarketValue = computed(
  () => players.value.reduce((sum, p) => sum + p.marketValue, 0),
)

const positionStats = computed(() =>
  positions.map(position => ({
    name: position,
    count: players.value.filter(p => p.position === position).length,
    percentage: players.value.length
      ? (players.value.filter(p => p.position === position).length /
          players.value.length) * 100
      : 0,
  })),
)

const filteredPlayers = computed(() => {
  const term = search.value.trim().toLowerCase()

  const result = players.value.filter(player => {
    const matchesSearch =
      !term ||
      player.name.toLowerCase().includes(term) ||
      player.team.toLowerCase().includes(term) ||
      player.nationality.toLowerCase().includes(term)

    const matchesPosition =
      positionFilter.value === 'All' ||
      player.position === positionFilter.value

    const matchesStatus =
      statusFilter.value === 'All' ||
      player.status === statusFilter.value

    const matchesTeam =
      teamFilter.value === 'All' ||
      player.team === teamFilter.value

    return matchesSearch && matchesPosition && matchesStatus && matchesTeam
  })

  return result.sort((a, b) => {
    if (sortBy.value === 'name') {
      return a.name.localeCompare(b.name)
    }

    if (sortBy.value === 'value') {
      return b.marketValue - a.marketValue
    }

    return b.goals - a.goals
  })
})

function getToken() {
  return localStorage.getItem('fids_access_token')
}

async function apiRequest<T>(
  url: string,
  options: RequestInit = {},
): Promise<T> {
  const token = getToken()

  if (!token) {
    throw new Error('Please log in to access player management.')
  }

  const headers = new Headers(options.headers)
  headers.set('Authorization', `Bearer ${token}`)

  if (options.body) {
    headers.set('Content-Type', 'application/json')
  }

  const response = await fetch(url, {
    ...options,
    headers,
  })

  if (response.status === 401) {
    throw new Error('Your session has expired. Please log in again.')
  }

  if (response.status === 204) {
    return undefined as T
  }

  const data = await response.json().catch(() => null)

  if (!response.ok) {
    const message =
      data?.detail ||
      data?.message ||
      Object.entries(data || {})
        .map(([key, value]) => `${key}: ${String(value)}`)
        .join(', ') ||
      `Server error: ${response.status}`

    throw new Error(message)
  }

  return data as T
}

function mapPlayer(item: ApiPlayer): Player {
  const teamName =
    typeof item.team === 'object'
      ? item.team?.name || ''
      : item.team || ''

  return {
    id: item.id,
    name: item.name || '',
    nationality: item.nationality || '',
    team: teamName,
    position: item.position || 'Midfielder',
    age: Number(item.age || 0),
    number: Number(item.number || 0),
    appearances: Number(item.appearances || 0),
    goals: Number(item.goals || 0),
    assists: Number(item.assists || 0),
    marketValue: Number(item.market_value ?? item.marketValue ?? 0),
    status: item.status || 'Active',
    photo: item.photo || item.image || '',
  }
}

function playerPayload() {
  return {
    name: form.value.name.trim(),
    nationality: form.value.nationality.trim(),
    team: form.value.team.trim(),
    position: form.value.position,
    age: Number(form.value.age),
    number: Number(form.value.number),
    appearances: Number(form.value.appearances),
    goals: Number(form.value.goals),
    assists: Number(form.value.assists),
    market_value: Number(form.value.marketValue),
    status: form.value.status,
    photo: form.value.photo.trim(),
  }
}

async function fetchPlayers() {
  loading.value = true
  errorMessage.value = ''

  try {
    let nextUrl: string | null = API_URL
    const allPlayers: ApiPlayer[] = []

    // Fetch every page when Django REST pagination is enabled.
    while (nextUrl) {
      const response = await apiRequest<
        ApiPlayer[] | PaginatedResponse<ApiPlayer>
      >(nextUrl)

      if (Array.isArray(response)) {
        allPlayers.push(...response)
        nextUrl = null
      } else {
        allPlayers.push(...(response.results || []))
        nextUrl = response.next || null
      }
    }

    players.value = allPlayers.map(mapPlayer)
  } catch (error) {
    errorMessage.value =
      error instanceof Error ? error.message : 'Unable to load players.'
  } finally {
    loading.value = false
  }
}

function formatValue(value: number) {
  if (value >= 1_000_000_000) {
    return `€${(value / 1_000_000_000).toFixed(1)}B`
  }

  if (value >= 1_000_000) {
    return `€${(value / 1_000_000).toFixed(1)}M`
  }

  if (value >= 1_000) {
    return `€${(value / 1_000).toFixed(0)}K`
  }

  return `€${value}`
}

function initials(name: string) {
  return name
    .split(' ')
    .filter(Boolean)
    .slice(0, 2)
    .map(part => part[0])
    .join('')
    .toUpperCase()
}

function statusClass(status: PlayerStatus) {
  return {
    Active: 'bg-emerald-500/10 text-emerald-400 ring-emerald-500/20',
    Injured: 'bg-rose-500/10 text-rose-400 ring-rose-500/20',
    Inactive: 'bg-slate-500/10 text-slate-400 ring-slate-500/20',
  }[status]
}

function positionClass(position: Position) {
  return {
    Goalkeeper: 'bg-amber-500/10 text-amber-400',
    Defender: 'bg-sky-500/10 text-sky-400',
    Midfielder: 'bg-violet-500/10 text-violet-400',
    Forward: 'bg-emerald-500/10 text-emerald-400',
  }[position]
}

function openCreate() {
  editingId.value = null
  form.value = emptyForm()
  formError.value = ''
  showEditor.value = true
}

function openEdit(player: Player) {
  editingId.value = player.id

  form.value = {
    name: player.name,
    nationality: player.nationality,
    team: player.team,
    position: player.position,
    age: player.age,
    number: player.number,
    appearances: player.appearances,
    goals: player.goals,
    assists: player.assists,
    marketValue: player.marketValue,
    status: player.status,
    photo: player.photo,
  }

  formError.value = ''
  showEditor.value = true
}

function validateForm() {
  if (!form.value.name.trim()) {
    formError.value = 'Player name is required.'
    return false
  }

  if (!form.value.team.trim()) {
    formError.value = 'Team name is required.'
    return false
  }

  const numbers = [
    form.value.age,
    form.value.number,
    form.value.appearances,
    form.value.goals,
    form.value.assists,
    form.value.marketValue,
  ]

  if (
    !numbers.every(Number.isFinite) ||
    form.value.age < 15 ||
    form.value.age > 60 ||
    numbers.slice(1).some(value => value < 0)
  ) {
    formError.value = 'Please enter valid player statistics.'
    return false
  }

  const duplicate = players.value.some(
    player =>
      player.number === form.value.number &&
      player.team.toLowerCase() === form.value.team.trim().toLowerCase() &&
      player.id !== editingId.value,
  )

  if (duplicate) {
    formError.value = 'This shirt number is already assigned to this team.'
    return false
  }

  return true
}

async function savePlayer() {
  formError.value = ''
  successMessage.value = ''

  if (!validateForm()) return

  saving.value = true

  try {
    const payload = playerPayload()

    if (editingId.value !== null) {
      await apiRequest(`${API_URL}${editingId.value}/`, {
        method: 'PATCH',
        body: JSON.stringify(payload),
      })

      successMessage.value = 'Player updated successfully.'
    } else {
      await apiRequest(API_URL, {
        method: 'POST',
        body: JSON.stringify(payload),
      })

      successMessage.value = 'Player created successfully.'
    }

    showEditor.value = false
    await fetchPlayers()
  } catch (error) {
    formError.value =
      error instanceof Error ? error.message : 'Unable to save player.'
  } finally {
    saving.value = false
  }
}

function viewPlayer(player: Player) {
  selectedPlayer.value = player
  showDetails.value = true
}

async function deletePlayer(player: Player) {
  const confirmed = window.confirm(
    `Are you sure you want to delete ${player.name}?`,
  )

  if (!confirmed) return

  errorMessage.value = ''
  successMessage.value = ''

  try {
    await apiRequest(`${API_URL}${player.id}/`, {
      method: 'DELETE',
    })

    if (selectedPlayer.value?.id === player.id) {
      selectedPlayer.value = null
      showDetails.value = false
    }

    successMessage.value = 'Player deleted successfully.'
    await fetchPlayers()
  } catch (error) {
    errorMessage.value =
      error instanceof Error ? error.message : 'Unable to delete player.'
  }
}

function closeEditor() {
  showEditor.value = false
  formError.value = ''
}

function clearFilters() {
  search.value = ''
  positionFilter.value = 'All'
  statusFilter.value = 'All'
  teamFilter.value = 'All'
  sortBy.value = 'goals'
}

function dismissMessages() {
  errorMessage.value = ''
  successMessage.value = ''
}

onMounted(fetchPlayers)
</script>

<template>
  <main class="min-h-screen space-y-7 bg-[#090d16] p-4 text-slate-100 sm:p-6 lg:p-8">
    <div class="mx-auto max-w-[1600px] space-y-7">

      <!-- Header -->
      <header class="flex flex-col justify-between gap-5 sm:flex-row sm:items-center">
        <div>
          <div class="mb-3 flex items-center gap-2 text-xs font-semibold uppercase tracking-[0.2em] text-slate-500">
            <span>FIDS</span>
            <span>/</span>
            <span>Admin</span>
            <span>/</span>
            <span class="text-cyan-400">Players</span>
          </div>

          <h1 class="text-3xl font-bold tracking-tight text-white sm:text-4xl">
            Players Management
          </h1>

          <p class="mt-2 text-sm text-slate-400">
            Manage player profiles, performance, squad availability and scouting data.
          </p>
        </div>

        <div class="flex flex-wrap gap-3">
          <button
            @click="fetchPlayers"
            :disabled="loading"
            class="flex items-center gap-2 rounded-xl border border-slate-700 bg-[#111827] px-4 py-3 text-sm font-medium text-slate-300 transition hover:border-cyan-500/50 hover:text-cyan-400 disabled:opacity-50"
          >
            <span>{{ loading ? 'Loading...' : '↻ Refresh' }}</span>
          </button>

          <button
            @click="openCreate"
            class="flex items-center gap-2 rounded-xl bg-cyan-400 px-5 py-3 text-sm font-bold text-slate-950 transition hover:bg-cyan-300"
          >
            <span class="text-lg">+</span>
            Add player
          </button>
        </div>
      </header>

      <!-- Notifications -->
      <div
        v-if="errorMessage"
        class="flex items-center justify-between rounded-xl border border-rose-500/20 bg-rose-500/10 px-4 py-3 text-sm text-rose-300"
      >
        <span>{{ errorMessage }}</span>
        <button @click="dismissMessages">✕</button>
      </div>

      <div
        v-if="successMessage"
        class="flex items-center justify-between rounded-xl border border-emerald-500/20 bg-emerald-500/10 px-4 py-3 text-sm text-emerald-300"
      >
        <span>{{ successMessage }}</span>
        <button @click="dismissMessages">✕</button>
      </div>

      <!-- Statistics -->
      <section class="grid grid-cols-1 gap-4 sm:grid-cols-2 xl:grid-cols-4">
        <article class="rounded-2xl border border-slate-800 bg-[#111827] p-5">
          <div class="flex items-center justify-between">
            <p class="text-sm text-slate-400">Total players</p>
            <span class="rounded-xl bg-cyan-500/10 p-3 text-cyan-400">♙</span>
          </div>
          <p class="mt-5 text-3xl font-bold text-white">{{ players.length }}</p>
          <p class="mt-2 text-xs text-slate-500">Registered profiles</p>
        </article>

        <article class="rounded-2xl border border-slate-800 bg-[#111827] p-5">
          <div class="flex items-center justify-between">
            <p class="text-sm text-slate-400">Active players</p>
            <span class="rounded-xl bg-emerald-500/10 p-3 text-emerald-400">✓</span>
          </div>
          <p class="mt-5 text-3xl font-bold text-white">{{ activeCount }}</p>
          <p class="mt-2 text-xs text-emerald-400">Available in squad</p>
        </article>

        <article class="rounded-2xl border border-slate-800 bg-[#111827] p-5">
          <div class="flex items-center justify-between">
            <p class="text-sm text-slate-400">Injured players</p>
            <span class="rounded-xl bg-rose-500/10 p-3 text-rose-400">+</span>
          </div>
          <p class="mt-5 text-3xl font-bold text-white">{{ injuredCount }}</p>
          <p class="mt-2 text-xs text-rose-400">Availability monitoring</p>
        </article>

        <article class="rounded-2xl border border-slate-800 bg-[#111827] p-5">
          <div class="flex items-center justify-between">
            <p class="text-sm text-slate-400">Squad market value</p>
            <span class="rounded-xl bg-violet-500/10 p-3 text-violet-400">€</span>
          </div>
          <p class="mt-5 text-3xl font-bold text-white">
            {{ formatValue(totalMarketValue) }}
          </p>
          <p class="mt-2 text-xs text-violet-400">Combined listed value</p>
        </article>
      </section>

      <!-- Analytics -->
      <section class="grid grid-cols-1 gap-5 xl:grid-cols-3">
        <article class="rounded-2xl border border-slate-800 bg-[#111827] p-6 xl:col-span-2">
          <div class="flex flex-col justify-between gap-3 sm:flex-row">
            <div>
              <h2 class="text-lg font-bold text-white">Squad analytics</h2>
              <p class="mt-1 text-sm text-slate-400">Player distribution by position</p>
            </div>

            <div class="flex gap-5 text-sm">
              <div>
                <p class="text-xs text-slate-500">Goals</p>
                <p class="mt-1 font-bold text-emerald-400">{{ totalGoals }}</p>
              </div>
              <div>
                <p class="text-xs text-slate-500">Assists</p>
                <p class="mt-1 font-bold text-cyan-400">{{ totalAssists }}</p>
              </div>
            </div>
          </div>

          <div class="mt-7 grid grid-cols-2 gap-4 xl:grid-cols-4">
            <div
              v-for="stat in positionStats"
              :key="stat.name"
              class="rounded-xl border border-slate-800 bg-[#090d16] p-4"
            >
              <p class="text-xs text-slate-400">{{ stat.name }}</p>
              <p class="mt-3 text-2xl font-bold text-white">{{ stat.count }}</p>
              <div class="mt-4 h-1.5 overflow-hidden rounded-full bg-slate-800">
                <div
                  class="h-full rounded-full bg-cyan-400 transition-all"
                  :style="{ width: `${stat.percentage}%` }"
                />
              </div>
              <p class="mt-2 text-xs text-slate-500">
                {{ stat.percentage.toFixed(0) }}% of squad
              </p>
            </div>
          </div>
        </article>

        <article class="flex flex-col justify-between rounded-2xl border border-cyan-500/20 bg-gradient-to-br from-cyan-500/10 to-[#111827] p-6">
          <div>
            <span class="text-xs font-bold uppercase tracking-[0.2em] text-cyan-400">
              FIDS Intelligence
            </span>
            <h2 class="mt-4 text-2xl font-bold text-white">
              Player performance
            </h2>
            <p class="mt-3 text-sm leading-7 text-slate-400">
              Monitor player statistics and squad information to support scouting and football decisions.
            </p>
          </div>

          <div class="mt-6 grid grid-cols-2 gap-3 border-t border-slate-700 pt-5">
            <div>
              <p class="text-xs text-slate-500">Appearances</p>
              <p class="mt-2 text-xl font-bold text-white">
                {{ players.reduce((sum, player) => sum + player.appearances, 0) }}
              </p>
            </div>
            <div>
              <p class="text-xs text-slate-500">Squad members</p>
              <p class="mt-2 text-xl font-bold text-cyan-400">{{ players.length }}</p>
            </div>
          </div>
        </article>
      </section>

      <!-- Players Directory -->
      <section class="overflow-hidden rounded-2xl border border-slate-800 bg-[#111827]">
        <div class="border-b border-slate-800 p-5 sm:p-6">
          <div class="flex flex-col justify-between gap-5 xl:flex-row xl:items-center">
            <div>
              <h2 class="text-xl font-bold text-white">Players directory</h2>
              <p class="mt-1 text-sm text-slate-400">
                {{ filteredPlayers.length }} players found
              </p>
            </div>

            <div class="grid grid-cols-1 gap-3 sm:grid-cols-2 xl:grid-cols-5">
              <input
                v-model="search"
                type="search"
                placeholder="Search players..."
                class="rounded-xl border border-slate-700 bg-[#090d16] px-4 py-3 text-sm text-white outline-none placeholder:text-slate-500 focus:border-cyan-400"
              />

              <select
                v-model="positionFilter"
                class="rounded-xl border border-slate-700 bg-[#090d16] px-3 py-3 text-sm text-slate-300 outline-none focus:border-cyan-400"
              >
                <option value="All">All positions</option>
                <option v-for="position in positions" :key="position" :value="position">
                  {{ position }}
                </option>
              </select>

              <select
                v-model="statusFilter"
                class="rounded-xl border border-slate-700 bg-[#090d16] px-3 py-3 text-sm text-slate-300 outline-none focus:border-cyan-400"
              >
                <option value="All">All statuses</option>
                <option value="Active">Active</option>
                <option value="Injured">Injured</option>
                <option value="Inactive">Inactive</option>
              </select>

              <select
                v-model="teamFilter"
                class="rounded-xl border border-slate-700 bg-[#090d16] px-3 py-3 text-sm text-slate-300 outline-none focus:border-cyan-400"
              >
                <option value="All">All teams</option>
                <option v-for="team in teams" :key="team" :value="team">
                  {{ team }}
                </option>
              </select>

              <select
                v-model="sortBy"
                class="rounded-xl border border-slate-700 bg-[#090d16] px-3 py-3 text-sm text-slate-300 outline-none focus:border-cyan-400"
              >
                <option value="goals">Most goals</option>
                <option value="name">Player name</option>
                <option value="value">Market value</option>
              </select>
            </div>
          </div>
        </div>

        <div class="overflow-x-auto">
          <table class="w-full min-w-[1100px] text-left">
            <thead class="bg-[#090d16] text-xs uppercase tracking-wider text-slate-500">
              <tr>
                <th class="px-5 py-4 font-semibold">Player</th>
                <th class="px-5 py-4 font-semibold">Position</th>
                <th class="px-5 py-4 font-semibold">Age</th>
                <th class="px-5 py-4 font-semibold">Apps</th>
                <th class="px-5 py-4 font-semibold">Goals</th>
                <th class="px-5 py-4 font-semibold">Assists</th>
                <th class="px-5 py-4 font-semibold">Market value</th>
                <th class="px-5 py-4 font-semibold">Status</th>
                <th class="px-5 py-4 text-right font-semibold">Actions</th>
              </tr>
            </thead>

            <tbody class="divide-y divide-slate-800">
              <tr v-if="loading">
                <td colspan="9" class="px-5 py-16 text-center text-slate-400">
                  Loading players from server...
                </td>
              </tr>

              <tr
                v-for="player in filteredPlayers"
                v-else
                :key="player.id"
                class="transition hover:bg-slate-800/30"
              >
                <td class="px-5 py-4">
                  <div class="flex items-center gap-3">
                    <img
                      v-if="player.photo"
                      :src="player.photo"
                      :alt="player.name"
                      class="h-11 w-11 rounded-full border border-slate-700 object-cover"
                    />
                    <div
                      v-else
                      class="flex h-11 w-11 shrink-0 items-center justify-center rounded-full bg-cyan-500/10 text-sm font-bold text-cyan-400"
                    >
                      {{ initials(player.name) }}
                    </div>

                    <div>
                      <p class="font-semibold text-white">{{ player.name }}</p>
                      <p class="mt-1 text-xs text-slate-500">
                        {{ player.team }} · {{ player.nationality || 'Unknown' }}
                      </p>
                    </div>
                  </div>
                </td>

                <td class="px-5 py-4">
                  <span
                    class="rounded-lg px-2.5 py-1.5 text-xs font-medium"
                    :class="positionClass(player.position)"
                  >
                    {{ player.position }}
                  </span>
                </td>

                <td class="px-5 py-4 text-sm text-slate-300">{{ player.age }}</td>
                <td class="px-5 py-4 text-sm text-slate-300">{{ player.appearances }}</td>
                <td class="px-5 py-4 text-sm font-bold text-white">{{ player.goals }}</td>
                <td class="px-5 py-4 text-sm text-slate-300">{{ player.assists }}</td>

                <td class="px-5 py-4 text-sm font-semibold text-cyan-400">
                  {{ formatValue(player.marketValue) }}
                </td>

                <td class="px-5 py-4">
                  <span
                    class="inline-flex rounded-full px-2.5 py-1 text-xs font-medium ring-1 ring-inset"
                    :class="statusClass(player.status)"
                  >
                    {{ player.status }}
                  </span>
                </td>

                <td class="px-5 py-4">
                  <div class="flex items-center justify-end gap-1">
                    <button
                      @click="viewPlayer(player)"
                      class="rounded-lg px-3 py-2 text-xs text-slate-300 transition hover:bg-slate-700 hover:text-white"
                    >
                      View
                    </button>

                    <button
                      @click="openEdit(player)"
                      class="rounded-lg px-3 py-2 text-xs text-cyan-400 transition hover:bg-cyan-500/10"
                    >
                      Edit
                    </button>

                    <button
                      @click="deletePlayer(player)"
                      class="rounded-lg px-3 py-2 text-xs text-rose-400 transition hover:bg-rose-500/10"
                    >
                      Delete
                    </button>
                  </div>
                </td>
              </tr>

              <tr v-if="!loading && filteredPlayers.length === 0">
                <td colspan="9" class="px-5 py-16 text-center">
                  <div class="mx-auto max-w-sm">
                    <div class="text-4xl text-slate-600">♙</div>
                    <p class="mt-4 font-semibold text-white">No players found</p>
                    <p class="mt-2 text-sm text-slate-500">
                      There are no players matching your search or filters.
                    </p>
                    <button
                      @click="clearFilters"
                      class="mt-4 text-sm font-semibold text-cyan-400 hover:text-cyan-300"
                    >
                      Clear filters
                    </button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <footer class="flex flex-col justify-between gap-2 border-t border-slate-800 px-5 py-4 text-xs text-slate-500 sm:flex-row">
          <span>Showing {{ filteredPlayers.length }} of {{ players.length }} players</span>
          <span>FIDS Admin · Player Intelligence</span>
        </footer>
      </section>
    </div>

    <!-- Create / Edit Modal -->
    <Teleport to="body">
      <div
        v-if="showEditor"
        class="fixed inset-0 z-[100] flex items-center justify-center overflow-y-auto bg-black/80 p-4 backdrop-blur-sm"
        @click.self="closeEditor"
      >
        <section class="my-auto max-h-[92vh] w-full max-w-3xl overflow-y-auto rounded-2xl border border-slate-700 bg-[#111827] shadow-2xl">
          <header class="sticky top-0 z-10 flex items-center justify-between border-b border-slate-800 bg-[#111827] px-6 py-5">
            <div>
              <h2 class="text-xl font-bold text-white">
                {{ editingId !== null ? 'Edit player' : 'Add new player' }}
              </h2>
              <p class="mt-1 text-sm text-slate-400">
                Enter player profile and performance information.
              </p>
            </div>

            <button
              @click="closeEditor"
              class="rounded-lg px-3 py-2 text-slate-400 hover:bg-slate-800 hover:text-white"
            >
              ✕
            </button>
          </header>

          <form class="space-y-6 p-6" @submit.prevent="savePlayer">
            <div>
              <h3 class="mb-4 text-sm font-bold uppercase tracking-wider text-cyan-400">
                Personal information
              </h3>

              <div class="grid grid-cols-1 gap-5 sm:grid-cols-2">
                <div>
                  <label class="mb-2 block text-sm text-slate-300">Full name *</label>
                  <input
                    v-model="form.name"
                    required
                    maxlength="120"
                    placeholder="Player full name"
                    class="w-full rounded-xl border border-slate-700 bg-[#090d16] px-4 py-3 text-sm text-white outline-none focus:border-cyan-400"
                  />
                </div>

                <div>
                  <label class="mb-2 block text-sm text-slate-300">Team *</label>
                  <input
                    v-model="form.team"
                    required
                    placeholder="Club or team"
                    class="w-full rounded-xl border border-slate-700 bg-[#090d16] px-4 py-3 text-sm text-white outline-none focus:border-cyan-400"
                  />
                </div>

                <div>
                  <label class="mb-2 block text-sm text-slate-300">Nationality</label>
                  <input
                    v-model="form.nationality"
                    placeholder="Country"
                    class="w-full rounded-xl border border-slate-700 bg-[#090d16] px-4 py-3 text-sm text-white outline-none focus:border-cyan-400"
                  />
                </div>

                <div>
                  <label class="mb-2 block text-sm text-slate-300">Photo URL</label>
                  <input
                    v-model="form.photo"
                    type="url"
                    placeholder="https://..."
                    class="w-full rounded-xl border border-slate-700 bg-[#090d16] px-4 py-3 text-sm text-white outline-none focus:border-cyan-400"
                  />
                </div>

                <div>
                  <label class="mb-2 block text-sm text-slate-300">Position *</label>
                  <select
                    v-model="form.position"
                    required
                    class="w-full rounded-xl border border-slate-700 bg-[#090d16] px-4 py-3 text-sm text-white outline-none focus:border-cyan-400"
                  >
                    <option v-for="position in positions" :key="position" :value="position">
                      {{ position }}
                    </option>
                  </select>
                </div>

                <div>
                  <label class="mb-2 block text-sm text-slate-300">Availability</label>
                  <select
                    v-model="form.status"
                    class="w-full rounded-xl border border-slate-700 bg-[#090d16] px-4 py-3 text-sm text-white outline-none focus:border-cyan-400"
                  >
                    <option value="Active">Active</option>
                    <option value="Injured">Injured</option>
                    <option value="Inactive">Inactive</option>
                  </select>
                </div>
              </div>
            </div>

            <div>
              <h3 class="mb-4 text-sm font-bold uppercase tracking-wider text-cyan-400">
                Player statistics
              </h3>

              <div class="grid grid-cols-2 gap-5 sm:grid-cols-3">
                <div>
                  <label class="mb-2 block text-sm text-slate-300">Age *</label>
                  <input
                    v-model.number="form.age"
                    type="number"
                    min="15"
                    max="60"
                    required
                    class="w-full rounded-xl border border-slate-700 bg-[#090d16] px-4 py-3 text-sm text-white outline-none focus:border-cyan-400"
                  />
                </div>

                <div>
                  <label class="mb-2 block text-sm text-slate-300">Shirt number</label>
                  <input
                    v-model.number="form.number"
                    type="number"
                    min="0"
                    required
                    class="w-full rounded-xl border border-slate-700 bg-[#090d16] px-4 py-3 text-sm text-white outline-none focus:border-cyan-400"
                  />
                </div>

                <div>
                  <label class="mb-2 block text-sm text-slate-300">Appearances</label>
                  <input
                    v-model.number="form.appearances"
                    type="number"
                    min="0"
                    required
                    class="w-full rounded-xl border border-slate-700 bg-[#090d16] px-4 py-3 text-sm text-white outline-none focus:border-cyan-400"
                  />
                </div>

                <div>
                  <label class="mb-2 block text-sm text-slate-300">Goals</label>
                  <input
                    v-model.number="form.goals"
                    type="number"
                    min="0"
                    required
                    class="w-full rounded-xl border border-slate-700 bg-[#090d16] px-4 py-3 text-sm text-white outline-none focus:border-cyan-400"
                  />
                </div>

                <div>
                  <label class="mb-2 block text-sm text-slate-300">Assists</label>
                  <input
                    v-model.number="form.assists"
                    type="number"
                    min="0"
                    required
                    class="w-full rounded-xl border border-slate-700 bg-[#090d16] px-4 py-3 text-sm text-white outline-none focus:border-cyan-400"
                  />
                </div>

                <div>
                  <label class="mb-2 block text-sm text-slate-300">Market value (€)</label>
                  <input
                    v-model.number="form.marketValue"
                    type="number"
                    min="0"
                    required
                    class="w-full rounded-xl border border-slate-700 bg-[#090d16] px-4 py-3 text-sm text-white outline-none focus:border-cyan-400"
                  />
                </div>
              </div>
            </div>

            <div
              v-if="formError"
              class="rounded-xl border border-rose-500/20 bg-rose-500/10 px-4 py-3 text-sm text-rose-300"
            >
              {{ formError }}
            </div>

            <footer class="flex flex-col-reverse gap-3 border-t border-slate-800 pt-5 sm:flex-row sm:justify-end">
              <button
                type="button"
                @click="closeEditor"
                class="rounded-xl border border-slate-700 px-5 py-3 text-sm text-slate-300 hover:bg-slate-800"
              >
                Cancel
              </button>

              <button
                type="submit"
                :disabled="saving"
                class="rounded-xl bg-cyan-400 px-6 py-3 text-sm font-bold text-slate-950 transition hover:bg-cyan-300 disabled:opacity-50"
              >
                {{
                  saving
                    ? 'Saving...'
                    : editingId !== null
                      ? 'Save changes'
                      : 'Create player'
                }}
              </button>
            </footer>
          </form>
        </section>
      </div>
    </Teleport>

    <!-- Player Details Modal -->
    <Teleport to="body">
      <div
        v-if="showDetails && selectedPlayer"
        class="fixed inset-0 z-[100] flex items-center justify-center overflow-y-auto bg-black/80 p-4 backdrop-blur-sm"
        @click.self="showDetails = false"
      >
        <section class="my-auto w-full max-w-xl overflow-hidden rounded-2xl border border-slate-700 bg-[#111827] shadow-2xl">
          <header class="flex items-center justify-between border-b border-slate-800 p-5">
            <div>
              <h2 class="text-lg font-bold text-white">Player profile</h2>
              <p class="mt-1 text-xs text-slate-500">Player intelligence details</p>
            </div>

            <button
              @click="showDetails = false"
              class="rounded-lg px-3 py-2 text-slate-400 hover:bg-slate-800"
            >
              ✕
            </button>
          </header>

          <div class="p-6">
            <div class="flex items-center gap-4">
              <img
                v-if="selectedPlayer.photo"
                :src="selectedPlayer.photo"
                :alt="selectedPlayer.name"
                class="h-20 w-20 rounded-2xl border border-slate-700 object-cover"
              />

              <div
                v-else
                class="flex h-20 w-20 items-center justify-center rounded-2xl bg-cyan-500/10 text-2xl font-bold text-cyan-400"
              >
                {{ initials(selectedPlayer.name) }}
              </div>

              <div class="min-w-0">
                <h3 class="text-xl font-bold text-white">
                  {{ selectedPlayer.name }}
                </h3>
                <p class="mt-1 text-sm text-slate-400">
                  {{ selectedPlayer.team }} · {{ selectedPlayer.nationality || 'Unknown' }}
                </p>

                <div class="mt-3 flex flex-wrap gap-2">
                  <span
                    class="rounded-lg px-2.5 py-1 text-xs"
                    :class="positionClass(selectedPlayer.position)"
                  >
                    {{ selectedPlayer.position }}
                  </span>

                  <span
                    class="rounded-full px-2.5 py-1 text-xs ring-1 ring-inset"
                    :class="statusClass(selectedPlayer.status)"
                  >
                    {{ selectedPlayer.status }}
                  </span>
                </div>
              </div>
            </div>

            <div class="mt-7 grid grid-cols-2 gap-3 sm:grid-cols-3">
              <div class="rounded-xl border border-slate-800 bg-[#090d16] p-4">
                <p class="text-xs text-slate-500">Age</p>
                <p class="mt-2 text-xl font-bold text-white">{{ selectedPlayer.age }}</p>
              </div>

              <div class="rounded-xl border border-slate-800 bg-[#090d16] p-4">
                <p class="text-xs text-slate-500">Shirt number</p>
                <p class="mt-2 text-xl font-bold text-white">#{{ selectedPlayer.number }}</p>
              </div>

              <div class="rounded-xl border border-slate-800 bg-[#090d16] p-4">
                <p class="text-xs text-slate-500">Appearances</p>
                <p class="mt-2 text-xl font-bold text-white">{{ selectedPlayer.appearances }}</p>
              </div>

              <div class="rounded-xl border border-slate-800 bg-[#090d16] p-4">
                <p class="text-xs text-slate-500">Goals</p>
                <p class="mt-2 text-xl font-bold text-emerald-400">{{ selectedPlayer.goals }}</p>
              </div>

              <div class="rounded-xl border border-slate-800 bg-[#090d16] p-4">
                <p class="text-xs text-slate-500">Assists</p>
                <p class="mt-2 text-xl font-bold text-cyan-400">{{ selectedPlayer.assists }}</p>
              </div>

              <div class="rounded-xl border border-slate-800 bg-[#090d16] p-4">
                <p class="text-xs text-slate-500">Market value</p>
                <p class="mt-2 text-lg font-bold text-cyan-400">
                  {{ formatValue(selectedPlayer.marketValue) }}
                </p>
              </div>
            </div>

            <footer class="mt-6 flex justify-end gap-3 border-t border-slate-800 pt-5">
              <button
                @click="showDetails = false"
                class="rounded-xl border border-slate-700 px-4 py-2.5 text-sm text-slate-300 hover:bg-slate-800"
              >
                Close
              </button>

              <button
                @click="openEdit(selectedPlayer!); showDetails = false"
                class="rounded-xl bg-cyan-400 px-4 py-2.5 text-sm font-bold text-slate-950 hover:bg-cyan-300"
              >
                Edit player
              </button>
            </footer>
          </div>
        </section>
      </div>
    </Teleport>
  </main>
</template>
