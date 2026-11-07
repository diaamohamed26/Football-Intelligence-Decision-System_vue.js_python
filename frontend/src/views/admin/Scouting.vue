
<script setup lang="ts">
import { computed, ref } from 'vue'

type Recommendation = 'High Priority' | 'Monitor' | 'Not Recommended'
type ScoutingStatus = 'Identified' | 'Watching' | 'Scouted' | 'Shortlisted'

interface Prospect {
  id: number
  name: string
  age: number
  nationality: string
  club: string
  position: string
  league: string
  potential: number
  rating: number
  marketValue: number
  status: ScoutingStatus
  recommendation: Recommendation
  scout: string
  notes: string
}

const prospects = ref<Prospect[]>([
  {
    id: 1,
    name: 'Omar Marmoush',
    age: 27,
    nationality: 'Egypt',
    club: 'Manchester City',
    position: 'Forward',
    league: 'Premier League',
    potential: 88,
    rating: 84,
    marketValue: 65000000,
    status: 'Scouted',
    recommendation: 'High Priority',
    scout: 'FIDS Scouting',
    notes: 'Attacking versatility, strong movement, and ability to create chances.',
  },
  {
    id: 2,
    name: 'Florian Wirtz',
    age: 23,
    nationality: 'Germany',
    club: 'Liverpool',
    position: 'Attacking Midfielder',
    league: 'Premier League',
    potential: 94,
    rating: 89,
    marketValue: 110000000,
    status: 'Shortlisted',
    recommendation: 'High Priority',
    scout: 'Ahmed Hassan',
    notes: 'Creative playmaker with excellent vision and ball progression.',
  },
  {
    id: 3,
    name: 'Lamine Yamal',
    age: 19,
    nationality: 'Spain',
    club: 'Barcelona',
    position: 'Winger',
    league: 'La Liga',
    potential: 97,
    rating: 91,
    marketValue: 180000000,
    status: 'Watching',
    recommendation: 'High Priority',
    scout: 'FIDS Academy',
    notes: 'Exceptional technical quality and one-on-one attacking ability.',
  },
  {
    id: 4,
    name: 'Adam Wharton',
    age: 22,
    nationality: 'England',
    club: 'Crystal Palace',
    position: 'Central Midfielder',
    league: 'Premier League',
    potential: 86,
    rating: 79,
    marketValue: 45000000,
    status: 'Identified',
    recommendation: 'Monitor',
    scout: 'Mohamed Ali',
    notes: 'Promising distribution and composure. Review consistency in high-pressure games.',
  },
  {
    id: 5,
    name: 'Alejandro Garnacho',
    age: 22,
    nationality: 'Argentina',
    club: 'Chelsea',
    position: 'Winger',
    league: 'Premier League',
    potential: 87,
    rating: 80,
    marketValue: 40000000,
    status: 'Watching',
    recommendation: 'Monitor',
    scout: 'Ahmed Hassan',
    notes: 'Direct attacker. Evaluate decision-making in the final third.',
  },
  {
    id: 6,
    name: 'Jorrel Hato',
    age: 20,
    nationality: 'Netherlands',
    club: 'Chelsea',
    position: 'Defender',
    league: 'Premier League',
    potential: 89,
    rating: 78,
    marketValue: 35000000,
    status: 'Identified',
    recommendation: 'Monitor',
    scout: 'FIDS Scouting',
    notes: 'Young defensive prospect with positional flexibility.',
  },
])

const search = ref('')
const statusFilter = ref<'All' | ScoutingStatus>('All')
const recommendationFilter = ref<'All' | Recommendation>('All')
const positionFilter = ref('All')
const sortBy = ref<'potential' | 'rating' | 'age' | 'marketValue'>('potential')

const showEditor = ref(false)
const showDetails = ref(false)
const editingId = ref<number | null>(null)
const selectedProspect = ref<Prospect | null>(null)
const formError = ref('')

const positions = computed(() =>
  [...new Set(prospects.value.map((prospect) => prospect.position))].sort(),
)

const highPriorityCount = computed(
  () =>
    prospects.value.filter(
      (prospect) => prospect.recommendation === 'High Priority',
    ).length,
)

const shortlistedCount = computed(
  () =>
    prospects.value.filter((prospect) => prospect.status === 'Shortlisted')
      .length,
)

const averagePotential = computed(() => {
  if (!prospects.value.length) return 0

  return Math.round(
    prospects.value.reduce((sum, prospect) => sum + prospect.potential, 0) /
      prospects.value.length,
  )
})

const totalMarketValue = computed(() =>
  prospects.value.reduce((sum, prospect) => sum + prospect.marketValue, 0),
)

const filteredProspects = computed(() => {
  const term = search.value.trim().toLowerCase()

  return prospects.value
    .filter((prospect) => {
      const matchesSearch =
        !term ||
        prospect.name.toLowerCase().includes(term) ||
        prospect.club.toLowerCase().includes(term) ||
        prospect.nationality.toLowerCase().includes(term) ||
        prospect.scout.toLowerCase().includes(term)

      const matchesStatus =
        statusFilter.value === 'All' ||
        prospect.status === statusFilter.value

      const matchesRecommendation =
        recommendationFilter.value === 'All' ||
        prospect.recommendation === recommendationFilter.value

      const matchesPosition =
        positionFilter.value === 'All' ||
        prospect.position === positionFilter.value

      return (
        matchesSearch &&
        matchesStatus &&
        matchesRecommendation &&
        matchesPosition
      )
    })
    .sort((a, b) => b[sortBy.value] - a[sortBy.value])
})

const emptyForm = (): Omit<Prospect, 'id'> => ({
  name: '',
  age: 18,
  nationality: '',
  club: '',
  position: 'Forward',
  league: '',
  potential: 70,
  rating: 60,
  marketValue: 0,
  status: 'Identified',
  recommendation: 'Monitor',
  scout: 'FIDS Scouting',
  notes: '',
})

const form = ref<Omit<Prospect, 'id'>>(emptyForm())

function formatMoney(value: number) {
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

function statusClass(status: ScoutingStatus) {
  const styles: Record<ScoutingStatus, string> = {
    Identified: 'bg-slate-500/10 text-slate-300 ring-slate-500/20',
    Watching: 'bg-sky-500/10 text-sky-400 ring-sky-500/20',
    Scouted: 'bg-violet-500/10 text-violet-400 ring-violet-500/20',
    Shortlisted: 'bg-emerald-500/10 text-emerald-400 ring-emerald-500/20',
  }

  return styles[status]
}

function recommendationClass(recommendation: Recommendation) {
  const styles: Record<Recommendation, string> = {
    'High Priority': 'bg-rose-500/10 text-rose-400',
    Monitor: 'bg-amber-500/10 text-amber-400',
    'Not Recommended': 'bg-slate-500/10 text-slate-400',
  }

  return styles[recommendation]
}

function scoreClass(score: number) {
  if (score >= 85) return 'text-emerald-400'
  if (score >= 70) return 'text-amber-400'
  return 'text-rose-400'
}

function openCreate() {
  editingId.value = null
  form.value = emptyForm()
  formError.value = ''
  showEditor.value = true
}

function openEdit(prospect: Prospect) {
  editingId.value = prospect.id
  const { id, ...editable } = prospect
  form.value = { ...editable }
  formError.value = ''
  showEditor.value = true
}

function saveProspect() {
  formError.value = ''

  if (!form.value.name.trim() || !form.value.club.trim()) {
    formError.value = 'Player name and current club are required.'
    return
  }

  if (
    form.value.age < 15 ||
    form.value.age > 50 ||
    form.value.potential < 0 ||
    form.value.potential > 100 ||
    form.value.rating < 0 ||
    form.value.rating > 100 ||
    form.value.marketValue < 0
  ) {
    formError.value =
      'Enter a valid age, non-negative market value, and scores between 0 and 100.'
    return
  }

  const cleanData = {
    ...form.value,
    name: form.value.name.trim(),
    club: form.value.club.trim(),
    nationality: form.value.nationality.trim(),
  }

  if (editingId.value !== null) {
    const index = prospects.value.findIndex(
      (prospect) => prospect.id === editingId.value,
    )

    if (index !== -1) {
      prospects.value[index] = {
        ...cleanData,
        id: editingId.value,
      }
    }
  } else {
    prospects.value.unshift({
      ...cleanData,
      id: Math.max(0, ...prospects.value.map((prospect) => prospect.id)) + 1,
    })
  }

  showEditor.value = false
}

function viewProspect(prospect: Prospect) {
  selectedProspect.value = prospect
  showDetails.value = true
}

function deleteProspect(prospect: Prospect) {
  if (!window.confirm(`Delete scouting record for ${prospect.name}?`)) return

  prospects.value = prospects.value.filter((item) => item.id !== prospect.id)

  if (selectedProspect.value?.id === prospect.id) {
    selectedProspect.value = null
    showDetails.value = false
  }
}

function clearFilters() {
  search.value = ''
  statusFilter.value = 'All'
  recommendationFilter.value = 'All'
  positionFilter.value = 'All'
}

function closeEditor() {
  showEditor.value = false
  formError.value = ''
}
</script>

<template>
  <main class="min-h-screen bg-slate-950 px-4 py-6 text-slate-100 sm:px-6 lg:px-8">
    <div class="mx-auto max-w-7xl space-y-7">
      <!-- Header -->
      <header class="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
        <div>
          <div class="mb-2 flex items-center gap-2 text-sm text-slate-400">
            <span>Admin</span>
            <span>/</span>
            <span class="text-emerald-400">Scouting</span>
          </div>

          <h1 class="text-3xl font-bold tracking-tight text-white">
            Scouting Intelligence
          </h1>

          <p class="mt-2 text-sm text-slate-400">
            Discover prospects, evaluate potential, and manage scouting recommendations.
          </p>
        </div>

        <button
          type="button"
          @click="openCreate"
          class="inline-flex items-center justify-center gap-2 rounded-xl bg-emerald-500 px-5 py-3 text-sm font-semibold text-slate-950 transition hover:bg-emerald-400"
        >
          <span class="text-lg">+</span>
          Add prospect
        </button>
      </header>

      <!-- Stats -->
      <section class="grid grid-cols-1 gap-4 sm:grid-cols-2 xl:grid-cols-4">
        <article class="rounded-2xl border border-slate-800 bg-slate-900 p-5">
          <p class="text-sm text-slate-400">Tracked prospects</p>
          <p class="mt-4 text-3xl font-bold text-white">{{ prospects.length }}</p>
          <p class="mt-2 text-xs text-slate-500">Players in the scouting database</p>
        </article>

        <article class="rounded-2xl border border-slate-800 bg-slate-900 p-5">
          <p class="text-sm text-slate-400">High priority</p>
          <p class="mt-4 text-3xl font-bold text-rose-400">{{ highPriorityCount }}</p>
          <p class="mt-2 text-xs text-slate-500">Candidates requiring attention</p>
        </article>

        <article class="rounded-2xl border border-slate-800 bg-slate-900 p-5">
          <p class="text-sm text-slate-400">Shortlisted</p>
          <p class="mt-4 text-3xl font-bold text-emerald-400">{{ shortlistedCount }}</p>
          <p class="mt-2 text-xs text-slate-500">Advanced scouting candidates</p>
        </article>

        <article class="rounded-2xl border border-slate-800 bg-slate-900 p-5">
          <p class="text-sm text-slate-400">Average potential</p>
          <p class="mt-4 text-3xl font-bold text-white">{{ averagePotential }}<span class="text-lg text-slate-500">/100</span></p>
          <p class="mt-2 text-xs text-slate-500">Internal prospect assessment</p>
        </article>
      </section>

      <!-- Overview panels -->
      <section class="grid grid-cols-1 gap-4 lg:grid-cols-3">
        <article class="rounded-2xl border border-slate-800 bg-slate-900 p-5 lg:col-span-2">
          <div class="flex flex-col gap-2 sm:flex-row sm:items-center sm:justify-between">
            <div>
              <h2 class="text-lg font-semibold text-white">Scouting pipeline</h2>
              <p class="mt-1 text-sm text-slate-400">Prospect progression across review stages</p>
            </div>
            <span class="text-xs text-slate-500">Current records</span>
          </div>

          <div class="mt-6 space-y-5">
            <div
              v-for="stage in [
                { name: 'Identified', color: 'bg-slate-400' },
                { name: 'Watching', color: 'bg-sky-400' },
                { name: 'Scouted', color: 'bg-violet-400' },
                { name: 'Shortlisted', color: 'bg-emerald-400' },
              ]"
              :key="stage.name"
            >
              <div class="mb-2 flex items-center justify-between text-sm">
                <span class="text-slate-300">{{ stage.name }}</span>
                <span class="text-slate-400">
                  {{ prospects.filter((prospect) => prospect.status === stage.name).length }}
                </span>
              </div>
              <div class="h-2 overflow-hidden rounded-full bg-slate-800">
                <div
                  :class="stage.color"
                  class="h-full rounded-full transition-all"
                  :style="{
                    width: `${prospects.length ? (prospects.filter((prospect) => prospect.status === stage.name).length / prospects.length) * 100 : 0}%`,
                  }"
                />
              </div>
            </div>
          </div>
        </article>

        <article class="rounded-2xl border border-emerald-500/20 bg-gradient-to-br from-emerald-500/10 to-slate-900 p-5">
          <span class="text-xs font-semibold uppercase tracking-widest text-emerald-400">
            Market intelligence
          </span>
          <h2 class="mt-3 text-xl font-bold text-white">Prospect valuation</h2>
          <p class="mt-2 text-sm leading-6 text-slate-400">
            Combined estimated market value of tracked prospects.
          </p>
          <p class="mt-5 text-3xl font-bold text-emerald-400">
            {{ formatMoney(totalMarketValue) }}
          </p>
          <p class="mt-2 text-xs text-slate-500">
            Illustrative values; not live transfer-market data.
          </p>
        </article>
      </section>

      <!-- Filters and table -->
      <section class="overflow-hidden rounded-2xl border border-slate-800 bg-slate-900">
        <div class="border-b border-slate-800 p-5">
          <div class="flex flex-col gap-4 xl:flex-row xl:items-center xl:justify-between">
            <div>
              <h2 class="text-lg font-semibold text-white">Prospect database</h2>
              <p class="mt-1 text-sm text-slate-400">
                {{ filteredProspects.length }} prospects found
              </p>
            </div>

            <div class="grid grid-cols-1 gap-3 sm:grid-cols-2 xl:grid-cols-5">
              <input
                v-model="search"
                type="search"
                placeholder="Search player, club..."
                class="rounded-xl border border-slate-700 bg-slate-950 px-4 py-2.5 text-sm text-white outline-none placeholder:text-slate-500 focus:border-emerald-500"
              />

              <select
                v-model="statusFilter"
                class="rounded-xl border border-slate-700 bg-slate-950 px-3 py-2.5 text-sm text-slate-200 outline-none focus:border-emerald-500"
              >
                <option value="All">All stages</option>
                <option value="Identified">Identified</option>
                <option value="Watching">Watching</option>
                <option value="Scouted">Scouted</option>
                <option value="Shortlisted">Shortlisted</option>
              </select>

              <select
                v-model="recommendationFilter"
                class="rounded-xl border border-slate-700 bg-slate-950 px-3 py-2.5 text-sm text-slate-200 outline-none focus:border-emerald-500"
              >
                <option value="All">All recommendations</option>
                <option value="High Priority">High Priority</option>
                <option value="Monitor">Monitor</option>
                <option value="Not Recommended">Not Recommended</option>
              </select>

              <select
                v-model="positionFilter"
                class="rounded-xl border border-slate-700 bg-slate-950 px-3 py-2.5 text-sm text-slate-200 outline-none focus:border-emerald-500"
              >
                <option value="All">All positions</option>
                <option v-for="position in positions" :key="position" :value="position">
                  {{ position }}
                </option>
              </select>

              <select
                v-model="sortBy"
                class="rounded-xl border border-slate-700 bg-slate-950 px-3 py-2.5 text-sm text-slate-200 outline-none focus:border-emerald-500"
              >
                <option value="potential">Sort: Potential</option>
                <option value="rating">Sort: Rating</option>
                <option value="age">Sort: Age</option>
                <option value="marketValue">Sort: Market value</option>
              </select>
            </div>
          </div>
        </div>

        <div class="overflow-x-auto">
          <table class="w-full min-w-[1100px] text-left">
            <thead class="bg-slate-950/70 text-xs uppercase tracking-wider text-slate-500">
              <tr>
                <th class="px-5 py-4 font-medium">Prospect</th>
                <th class="px-5 py-4 font-medium">Position</th>
                <th class="px-5 py-4 font-medium">Age</th>
                <th class="px-5 py-4 font-medium">Rating</th>
                <th class="px-5 py-4 font-medium">Potential</th>
                <th class="px-5 py-4 font-medium">Market value</th>
                <th class="px-5 py-4 font-medium">Stage</th>
                <th class="px-5 py-4 font-medium">Recommendation</th>
                <th class="px-5 py-4 text-right font-medium">Actions</th>
              </tr>
            </thead>

            <tbody class="divide-y divide-slate-800">
              <tr
                v-for="prospect in filteredProspects"
                :key="prospect.id"
                class="transition hover:bg-slate-800/40"
              >
                <td class="px-5 py-4">
                  <div class="flex items-center gap-3">
                    <div class="flex h-11 w-11 shrink-0 items-center justify-center rounded-xl bg-emerald-500/10 font-bold text-emerald-400">
                      {{ prospect.name.split(' ').map((part) => part[0]).slice(0, 2).join('') }}
                    </div>
                    <div>
                      <p class="font-semibold text-white">{{ prospect.name }}</p>
                      <p class="mt-1 text-xs text-slate-500">
                        {{ prospect.club }} · {{ prospect.nationality }}
                      </p>
                    </div>
                  </div>
                </td>

                <td class="px-5 py-4 text-sm text-slate-300">{{ prospect.position }}</td>
                <td class="px-5 py-4 text-sm text-slate-300">{{ prospect.age }}</td>

                <td class="px-5 py-4">
                  <span class="font-semibold" :class="scoreClass(prospect.rating)">
                    {{ prospect.rating }}
                  </span>
                  <span class="text-xs text-slate-600">/100</span>
                </td>

                <td class="px-5 py-4">
                  <div class="flex items-center gap-2">
                    <span class="font-semibold" :class="scoreClass(prospect.potential)">
                      {{ prospect.potential }}
                    </span>
                    <div class="h-1.5 w-14 overflow-hidden rounded-full bg-slate-800">
                      <div
                        class="h-full rounded-full bg-emerald-400"
                        :style="{ width: `${prospect.potential}%` }"
                      />
                    </div>
                  </div>
                </td>

                <td class="px-5 py-4 text-sm font-medium text-white">
                  {{ formatMoney(prospect.marketValue) }}
                </td>

                <td class="px-5 py-4">
                  <span
                    class="inline-flex rounded-full px-2.5 py-1 text-xs font-medium ring-1 ring-inset"
                    :class="statusClass(prospect.status)"
                  >
                    {{ prospect.status }}
                  </span>
                </td>

                <td class="px-5 py-4">
                  <span
                    class="rounded-lg px-2.5 py-1.5 text-xs font-medium"
                    :class="recommendationClass(prospect.recommendation)"
                  >
                    {{ prospect.recommendation }}
                  </span>
                </td>

                <td class="px-5 py-4">
                  <div class="flex items-center justify-end gap-1">
                    <button
                      type="button"
                      @click="viewProspect(prospect)"
                      class="rounded-lg px-2.5 py-2 text-xs text-slate-300 hover:bg-slate-700 hover:text-white"
                    >
                      View
                    </button>
                    <button
                      type="button"
                      @click="openEdit(prospect)"
                      class="rounded-lg px-2.5 py-2 text-xs text-emerald-400 hover:bg-emerald-500/10"
                    >
                      Edit
                    </button>
                    <button
                      type="button"
                      @click="deleteProspect(prospect)"
                      class="rounded-lg px-2.5 py-2 text-xs text-rose-400 hover:bg-rose-500/10"
                    >
                      Delete
                    </button>
                  </div>
                </td>
              </tr>

              <tr v-if="filteredProspects.length === 0">
                <td colspan="9" class="px-5 py-16 text-center">
                  <p class="font-medium text-white">No prospects found</p>
                  <p class="mt-1 text-sm text-slate-500">
                    Try another search term or change your filters.
                  </p>
                  <button
                    type="button"
                    @click="clearFilters"
                    class="mt-4 text-sm font-medium text-emerald-400 hover:text-emerald-300"
                  >
                    Clear filters
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <footer class="flex flex-col gap-2 border-t border-slate-800 px-5 py-4 text-xs text-slate-500 sm:flex-row sm:items-center sm:justify-between">
          <p>Showing {{ filteredProspects.length }} of {{ prospects.length }} prospects</p>
          <p>FIDS Admin · Scouting Intelligence</p>
        </footer>
      </section>
    </div>

    <!-- Add / Edit modal -->
    <div
      v-if="showEditor"
      class="fixed inset-0 z-50 flex items-center justify-center overflow-y-auto bg-black/70 p-4 backdrop-blur-sm"
      @click.self="closeEditor"
    >
      <section class="my-auto max-h-[92vh] w-full max-w-2xl overflow-y-auto rounded-2xl border border-slate-700 bg-slate-900 shadow-2xl">
        <header class="sticky top-0 z-10 flex items-center justify-between border-b border-slate-800 bg-slate-900 px-6 py-5">
          <div>
            <h2 class="text-xl font-bold text-white">
              {{ editingId !== null ? 'Edit prospect' : 'Add prospect' }}
            </h2>
            <p class="mt-1 text-sm text-slate-400">Prospect profile and scouting assessment.</p>
          </div>
          <button type="button" @click="closeEditor" class="rounded-lg px-3 py-2 text-slate-400 hover:bg-slate-800 hover:text-white">
            ✕
          </button>
        </header>

        <form class="space-y-5 p-6" @submit.prevent="saveProspect">
          <div class="grid grid-cols-1 gap-5 sm:grid-cols-2">
            <div>
              <label class="mb-2 block text-sm font-medium text-slate-300">Player name *</label>
              <input v-model="form.name" required maxlength="120" placeholder="Full name" class="w-full rounded-xl border border-slate-700 bg-slate-950 px-4 py-3 text-sm text-white outline-none focus:border-emerald-500" />
            </div>

            <div>
              <label class="mb-2 block text-sm font-medium text-slate-300">Current club *</label>
              <input v-model="form.club" required placeholder="Club name" class="w-full rounded-xl border border-slate-700 bg-slate-950 px-4 py-3 text-sm text-white outline-none focus:border-emerald-500" />
            </div>

            <div>
              <label class="mb-2 block text-sm font-medium text-slate-300">Nationality</label>
              <input v-model="form.nationality" placeholder="Country" class="w-full rounded-xl border border-slate-700 bg-slate-950 px-4 py-3 text-sm text-white outline-none focus:border-emerald-500" />
            </div>

            <div>
              <label class="mb-2 block text-sm font-medium text-slate-300">Position</label>
              <input v-model="form.position" required placeholder="e.g. Winger" class="w-full rounded-xl border border-slate-700 bg-slate-950 px-4 py-3 text-sm text-white outline-none focus:border-emerald-500" />
            </div>

            <div>
              <label class="mb-2 block text-sm font-medium text-slate-300">League</label>
              <input v-model="form.league" placeholder="League name" class="w-full rounded-xl border border-slate-700 bg-slate-950 px-4 py-3 text-sm text-white outline-none focus:border-emerald-500" />
            </div>

            <div>
              <label class="mb-2 block text-sm font-medium text-slate-300">Age</label>
              <input v-model.number="form.age" type="number" min="15" max="50" required class="w-full rounded-xl border border-slate-700 bg-slate-950 px-4 py-3 text-sm text-white outline-none focus:border-emerald-500" />
            </div>

            <div>
              <label class="mb-2 block text-sm font-medium text-slate-300">Current rating (0–100)</label>
              <input v-model.number="form.rating" type="number" min="0" max="100" required class="w-full rounded-xl border border-slate-700 bg-slate-950 px-4 py-3 text-sm text-white outline-none focus:border-emerald-500" />
            </div>

            <div>
              <label class="mb-2 block text-sm font-medium text-slate-300">Potential (0–100)</label>
              <input v-model.number="form.potential" type="number" min="0" max="100" required class="w-full rounded-xl border border-slate-700 bg-slate-950 px-4 py-3 text-sm text-white outline-none focus:border-emerald-500" />
            </div>

            <div>
              <label class="mb-2 block text-sm font-medium text-slate-300">Estimated market value (€)</label>
              <input v-model.number="form.marketValue" type="number" min="0" required class="w-full rounded-xl border border-slate-700 bg-slate-950 px-4 py-3 text-sm text-white outline-none focus:border-emerald-500" />
            </div>

            <div>
              <label class="mb-2 block text-sm font-medium text-slate-300">Scouting stage</label>
              <select v-model="form.status" class="w-full rounded-xl border border-slate-700 bg-slate-950 px-3 py-3 text-sm text-white outline-none focus:border-emerald-500">
                <option value="Identified">Identified</option>
                <option value="Watching">Watching</option>
                <option value="Scouted">Scouted</option>
                <option value="Shortlisted">Shortlisted</option>
              </select>
            </div>

            <div>
              <label class="mb-2 block text-sm font-medium text-slate-300">Recommendation</label>
              <select v-model="form.recommendation" class="w-full rounded-xl border border-slate-700 bg-slate-950 px-3 py-3 text-sm text-white outline-none focus:border-emerald-500">
                <option value="High Priority">High Priority</option>
                <option value="Monitor">Monitor</option>
                <option value="Not Recommended">Not Recommended</option>
              </select>
            </div>

            <div>
              <label class="mb-2 block text-sm font-medium text-slate-300">Assigned scout</label>
              <input v-model="form.scout" placeholder="Scout name or team" class="w-full rounded-xl border border-slate-700 bg-slate-950 px-4 py-3 text-sm text-white outline-none focus:border-emerald-500" />
            </div>
          </div>

          <div>
            <label class="mb-2 block text-sm font-medium text-slate-300">Scouting notes</label>
            <textarea v-model="form.notes" rows="4" placeholder="Strengths, weaknesses, tactical fit, and follow-up actions..." class="w-full resize-y rounded-xl border border-slate-700 bg-slate-950 px-4 py-3 text-sm text-white outline-none focus:border-emerald-500" />
          </div>

          <p v-if="formError" class="rounded-lg border border-rose-500/20 bg-rose-500/10 px-4 py-3 text-sm text-rose-300">
            {{ formError }}
          </p>

          <footer class="flex flex-col-reverse gap-3 border-t border-slate-800 pt-5 sm:flex-row sm:justify-end">
            <button type="button" @click="closeEditor" class="rounded-xl border border-slate-700 px-5 py-3 text-sm font-medium text-slate-300 hover:bg-slate-800">
              Cancel
            </button>
            <button type="submit" class="rounded-xl bg-emerald-500 px-5 py-3 text-sm font-semibold text-slate-950 hover:bg-emerald-400">
              {{ editingId !== null ? 'Save changes' : 'Add prospect' }}
            </button>
          </footer>
        </form>
      </section>
    </div>

    <!-- Prospect details -->
    <div
      v-if="showDetails && selectedProspect"
      class="fixed inset-0 z-50 flex items-center justify-center overflow-y-auto bg-black/70 p-4 backdrop-blur-sm"
      @click.self="showDetails = false"
    >
      <section class="my-auto w-full max-w-2xl overflow-hidden rounded-2xl border border-slate-700 bg-slate-900 shadow-2xl">
        <header class="flex items-center justify-between border-b border-slate-800 p-5">
          <h2 class="text-lg font-bold text-white">Scouting report</h2>
          <button type="button" @click="showDetails = false" class="rounded-lg px-3 py-2 text-slate-400 hover:bg-slate-800 hover:text-white">
            ✕
          </button>
        </header>

        <div class="space-y-6 p-6">
          <div class="flex items-center gap-4">
            <div class="flex h-16 w-16 items-center justify-center rounded-2xl bg-emerald-500/10 text-xl font-bold text-emerald-400">
              {{ selectedProspect.name.split(' ').map((part) => part[0]).slice(0, 2).join('') }}
            </div>
            <div>
              <h3 class="text-xl font-bold text-white">{{ selectedProspect.name }}</h3>
              <p class="mt-1 text-sm text-slate-400">
                {{ selectedProspect.club }} · {{ selectedProspect.nationality }}
              </p>
              <p class="mt-1 text-xs text-slate-500">
                {{ selectedProspect.position }} · {{ selectedProspect.league || 'League not specified' }} · Age {{ selectedProspect.age }}
              </p>
            </div>
          </div>

          <div class="grid grid-cols-2 gap-3 sm:grid-cols-4">
            <div class="rounded-xl border border-slate-800 bg-slate-950 p-4">
              <p class="text-xs text-slate-500">Rating</p>
              <p class="mt-2 text-2xl font-bold" :class="scoreClass(selectedProspect.rating)">
                {{ selectedProspect.rating }}
              </p>
            </div>
            <div class="rounded-xl border border-slate-800 bg-slate-950 p-4">
              <p class="text-xs text-slate-500">Potential</p>
              <p class="mt-2 text-2xl font-bold" :class="scoreClass(selectedProspect.potential)">
                {{ selectedProspect.potential }}
              </p>
            </div>
            <div class="rounded-xl border border-slate-800 bg-slate-950 p-4">
              <p class="text-xs text-slate-500">Market value</p>
              <p class="mt-2 text-lg font-bold text-white">{{ formatMoney(selectedProspect.marketValue) }}</p>
            </div>
            <div class="rounded-xl border border-slate-800 bg-slate-950 p-4">
              <p class="text-xs text-slate-500">Assigned scout</p>
              <p class="mt-2 text-sm font-semibold text-white">{{ selectedProspect.scout || 'Unassigned' }}</p>
            </div>
          </div>

          <div>
            <p class="text-sm font-semibold text-white">Scout notes</p>
            <p class="mt-2 whitespace-pre-wrap text-sm leading-7 text-slate-400">
              {{ selectedProspect.notes || 'No scouting notes added yet.' }}
            </p>
          </div>

          <div class="flex flex-wrap items-center gap-2">
            <span class="rounded-full px-3 py-1.5 text-xs ring-1 ring-inset" :class="statusClass(selectedProspect.status)">
              {{ selectedProspect.status }}
            </span>
            <span class="rounded-lg px-3 py-1.5 text-xs" :class="recommendationClass(selectedProspect.recommendation)">
              {{ selectedProspect.recommendation }}
            </span>
          </div>

          <footer class="flex justify-end gap-3 border-t border-slate-800 pt-5">
            <button type="button" @click="showDetails = false" class="rounded-xl border border-slate-700 px-4 py-2.5 text-sm text-slate-300 hover:bg-slate-800">
              Close
            </button>
            <button type="button" @click="openEdit(selectedProspect!); showDetails = false" class="rounded-xl bg-emerald-500 px-4 py-2.5 text-sm font-semibold text-slate-950 hover:bg-emerald-400">
              Edit prospect
            </button>
          </footer>
        </div>
      </section>
    </div>
  </main>
</template>