<script setup lang="ts">
import { computed, ref } from 'vue'
import { RouterLink, useRoute, useRouter } from 'vue-router'
import {
  Search as SearchIcon,
  X,
  ArrowRight,
  Users,
  UserRound,
  Trophy,
  Newspaper,
  Zap
} from 'lucide-vue-next'

const route = useRoute()
const router = useRouter()

const searchInput = ref(
  typeof route.query.q === 'string' ? route.query.q : ''
)

const query = ref(searchInput.value)

const activeFilter = ref<'all' | 'teams' | 'players' | 'matches' | 'news'>(
  'all'
)

const filters = [
  { id: 'all', label: 'All' },
  { id: 'teams', label: 'Teams' },
  { id: 'players', label: 'Players' },
  { id: 'matches', label: 'Matches' },
  { id: 'news', label: 'News' }
] as const

const demoResults = [
  {
    type: 'team',
    title: 'Manchester City',
    subtitle: 'Premier League',
    description: 'Football club',
    icon: Users,
    path: '/teams/1'
  },
  {
    type: 'team',
    title: 'Liverpool',
    subtitle: 'Premier League',
    description: 'Football club',
    icon: Users,
    path: '/teams/2'
  },
  {
    type: 'player',
    title: 'Erling Haaland',
    subtitle: 'Manchester City',
    description: 'Forward',
    icon: UserRound,
    path: '/players/1'
  },
  {
    type: 'player',
    title: 'Mohamed Salah',
    subtitle: 'Liverpool',
    description: 'Forward',
    icon: UserRound,
    path: '/players/2'
  },
  {
    type: 'match',
    title: 'Manchester City vs Liverpool',
    subtitle: 'Premier League',
    description: 'Match',
    icon: Trophy,
    path: '/matches/1'
  },
  {
    type: 'news',
    title: 'Latest Football News',
    subtitle: 'Football',
    description: 'News article',
    icon: Newspaper,
    path: '/news'
  }
]

const filteredResults = computed(() => {
  const search = query.value.trim().toLowerCase()

  if (!search) {
    return []
  }

  return demoResults.filter((item) => {
    const matchesFilter =
      activeFilter.value === 'all' ||
      item.type === activeFilter.value.slice(0, -1)

    const matchesSearch =
      item.title.toLowerCase().includes(search) ||
      item.subtitle.toLowerCase().includes(search) ||
      item.description.toLowerCase().includes(search)

    return matchesFilter && matchesSearch
  })
})

const performSearch = async () => {
  const value = query.value.trim()

  await router.replace({
    path: '/search',
    query: value ? { q: value } : {}
  })
}

const clearSearch = async () => {
  query.value = ''

  await router.replace({
    path: '/search'
  })
}
</script>

<template>
  <main class="min-h-[calc(100vh-72px)] bg-[#070A0F] text-white">
    <div class="mx-auto max-w-[1200px] px-4 py-10 sm:px-6 lg:px-8">

      <!-- Header -->
      <section class="mb-8">
        <div class="mb-3 flex items-center gap-2 text-[#B7FF3C]">
          <Zap :size="18" />
          <span class="text-xs font-bold uppercase tracking-[0.2em]">
            FIDS Intelligence
          </span>
        </div>

        <h1 class="text-3xl font-black tracking-tight sm:text-4xl">
          Search Football Data
        </h1>

        <p class="mt-2 max-w-2xl text-sm text-[#8993A4] sm:text-base">
          Search teams, players, matches and football news across FIDS.
        </p>
      </section>

      <!-- Search Box -->
      <section
        class="rounded-2xl border border-[#202936] bg-[#0F141C] p-4 shadow-xl"
      >
        <form
          class="flex flex-col gap-3 sm:flex-row"
          @submit.prevent="performSearch"
        >
          <div class="relative flex-1">
            <SearchIcon
              :size="20"
              class="absolute left-4 top-1/2 -translate-y-1/2 text-[#8993A4]"
            />

            <input
              v-model="query"
              type="search"
              placeholder="Search teams, players, matches..."
              autocomplete="off"
              class="h-12 w-full rounded-xl border border-[#202936] bg-[#070A0F] pl-12 pr-12 text-sm text-white outline-none transition placeholder:text-[#586273] focus:border-[#B7FF3C]/60"
              @keyup.enter="performSearch"
            />

            <button
              v-if="query"
              type="button"
              aria-label="Clear search"
              class="absolute right-3 top-1/2 flex h-8 w-8 -translate-y-1/2 items-center justify-center rounded-lg text-[#8993A4] transition hover:bg-[#151C26] hover:text-white"
              @click="clearSearch"
            >
              <X :size="17" />
            </button>
          </div>

          <button
            type="submit"
            class="h-12 rounded-xl bg-[#B7FF3C] px-6 text-sm font-black text-[#070A0F] transition hover:bg-[#c4ff5c]"
          >
            Search
          </button>
        </form>

        <!-- Filters -->
        <div class="mt-4 flex flex-wrap gap-2">
          <button
            v-for="filter in filters"
            :key="filter.id"
            type="button"
            class="rounded-lg px-4 py-2 text-xs font-semibold transition"
            :class="
              activeFilter === filter.id
                ? 'bg-[#B7FF3C] text-[#070A0F]'
                : 'bg-[#151C26] text-[#8993A4] hover:text-white'
            "
            @click="activeFilter = filter.id"
          >
            {{ filter.label }}
          </button>
        </div>
      </section>

      <!-- Empty State -->
      <section
        v-if="!query.trim()"
        class="flex min-h-[350px] flex-col items-center justify-center text-center"
      >
        <div
          class="mb-5 flex h-16 w-16 items-center justify-center rounded-2xl bg-[#151C26] text-[#B7FF3C]"
        >
          <SearchIcon :size="28" />
        </div>

        <h2 class="text-xl font-bold">
          Start your search
        </h2>

        <p class="mt-2 max-w-md text-sm text-[#8993A4]">
          Enter a team, player, match or news keyword to explore football
          intelligence.
        </p>
      </section>

      <!-- No Results -->
      <section
        v-else-if="filteredResults.length === 0"
        class="flex min-h-[350px] flex-col items-center justify-center text-center"
      >
        <div
          class="mb-5 flex h-16 w-16 items-center justify-center rounded-2xl bg-[#151C26] text-[#8993A4]"
        >
          <SearchIcon :size="28" />
        </div>

        <h2 class="text-xl font-bold">
          No results found
        </h2>

        <p class="mt-2 text-sm text-[#8993A4]">
          No results matched
          <span class="font-semibold text-white">
            "{{ query }}"
          </span>
        </p>
      </section>

      <!-- Results -->
      <section v-else class="mt-8">

        <div class="mb-4 flex items-center justify-between">
          <div>
            <h2 class="text-lg font-bold">
              Search Results
            </h2>

            <p class="mt-1 text-xs text-[#8993A4]">
              {{ filteredResults.length }} result{{
                filteredResults.length === 1 ? '' : 's'
              }}
            </p>
          </div>
        </div>

        <div class="grid gap-3">
          <RouterLink
            v-for="result in filteredResults"
            :key="`${result.type}-${result.title}`"
            :to="result.path"
            class="group flex items-center gap-4 rounded-2xl border border-[#202936] bg-[#0F141C] p-4 transition-all duration-200 hover:border-[#B7FF3C]/40 hover:bg-[#151C26]"
          >
            <div
              class="flex h-12 w-12 shrink-0 items-center justify-center rounded-xl bg-[#151C26] text-[#B7FF3C]"
            >
              <component
                :is="result.icon"
                :size="21"
              />
            </div>

            <div class="min-w-0 flex-1">
              <div class="truncate text-sm font-bold text-white">
                {{ result.title }}
              </div>

              <div class="mt-1 text-xs text-[#8993A4]">
                {{ result.subtitle }}
              </div>

              <div class="mt-1 text-[11px] uppercase tracking-wider text-[#586273]">
                {{ result.description }}
              </div>
            </div>

            <ArrowRight
              :size="18"
              class="shrink-0 text-[#586273] transition-transform duration-200 group-hover:translate-x-1 group-hover:text-[#B7FF3C]"
            />
          </RouterLink>
        </div>
      </section>
    </div>
  </main>
</template>
