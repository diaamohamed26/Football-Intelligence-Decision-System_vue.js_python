cat > src/views/Matches.vue <<'EOF'
<template>
  <section class="mx-auto max-w-7xl px-4 py-12">
    <PageHeader title="Matches" subtitle="Explore upcoming, live and completed matches." />

    <div class="mb-8 flex flex-wrap gap-3">
      <button
        v-for="filter in filters"
        :key="filter"
        class="rounded-xl border border-[#202936] bg-[#0F141C] px-4 py-2 text-sm hover:border-[#B7FF3C]"
      >
        {{ filter }}
      </button>
    </div>

    <div class="grid gap-4 lg:grid-cols-2">
      <MatchCard
        v-for="match in matches"
        :key="match.id"
        :match="match"
      />
    </div>
  </section>
</template>

<script setup lang="ts">
import PageHeader from '@/components/common/SectionTitle.vue'
import MatchCard from '@/components/matches/MatchCard.vue'

const filters = ['All', 'Today', 'Upcoming', 'Live', 'Completed']

const matches = [
  {
    id: '1',
    homeTeam: 'Al Ahly',
    awayTeam: 'Pyramids',
    homeScore: 0,
    awayScore: 0,
    time: '20:00',
    status: 'UPCOMING',
    competition: 'Egyptian Premier League',
  },
  {
    id: '2',
    homeTeam: 'Liverpool',
    awayTeam: 'Chelsea',
    homeScore: 2,
    awayScore: 1,
    time: 'FT',
    status: 'FT',
    competition: 'Premier League',
  },
]
</script>
EOF