cat > src/views/Competitions.vue <<'EOF'
<template>
  <section class="mx-auto max-w-7xl px-4 py-12">
    <PageHeader title="Competitions" subtitle="Football competitions tracked by FIDS." />

    <div class="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
      <div
        v-for="competition in competitions"
        :key="competition.name"
        class="rounded-2xl border border-[#202936] bg-[#0F141C] p-6 transition hover:border-[#B7FF3C]"
      >
        <div class="flex h-14 w-14 items-center justify-center rounded-xl bg-[#151C26] text-xl">
          {{ competition.icon }}
        </div>
        <h2 class="mt-5 text-xl font-bold">{{ competition.name }}</h2>
        <p class="mt-2 text-sm text-[#8993A4]">{{ competition.country }}</p>
        <p class="mt-4 text-sm text-[#8993A4]">
          {{ competition.teams }} teams
        </p>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import PageHeader from '@/components/common/SectionTitle.vue'

const competitions = [
  { name: 'Egyptian Premier League', country: 'Egypt', teams: 18, icon: 'EG' },
  { name: 'Premier League', country: 'England', teams: 20, icon: 'PL' },
  { name: 'La Liga', country: 'Spain', teams: 20, icon: 'ES' },
  { name: 'UEFA Champions League', country: 'Europe', teams: 36, icon: 'UCL' },
  { name: 'Serie A', country: 'Italy', teams: 20, icon: 'IT' },
  { name: 'Bundesliga', country: 'Germany', teams: 18, icon: 'DE' },
]
</script>
EOF
