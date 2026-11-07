cat > src/views/Live.vue <<'EOF'
<template>
  <section class="mx-auto max-w-7xl px-4 py-12">
    <PageHeader title="Live" subtitle="Live football matches and real-time intelligence." />

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

const matches = [
  {
    id: '1',
    homeTeam: 'Al Ahly',
    awayTeam: 'Zamalek',
    homeScore: 1,
    awayScore: 0,
    time: '67',
    status: 'LIVE',
    competition: 'Egyptian Premier League',
  },
  {
    id: '2',
    homeTeam: 'Liverpool',
    awayTeam: 'Arsenal',
    homeScore: 1,
    awayScore: 1,
    time: '52',
    status: 'LIVE',
    competition: 'Premier League',
  },
]
</script>
EOF