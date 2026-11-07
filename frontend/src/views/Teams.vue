cat > src/views/Teams.vue <<'EOF'
<template>
  <section class="mx-auto max-w-7xl px-4 py-12">
    <PageHeader title="Teams" subtitle="Discover teams, performance and tactical intelligence." />

    <div class="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
      <RouterLink
        v-for="team in teams"
        :key="team.id"
        :to="`/teams/${team.id}`"
        class="rounded-2xl border border-[#202936] bg-[#0F141C] p-6 hover:border-[#B7FF3C]"
      >
        <div class="flex h-16 w-16 items-center justify-center rounded-full bg-[#151C26] text-xl font-bold">
          {{ team.short }}
        </div>
        <h2 class="mt-5 font-bold">{{ team.name }}</h2>
        <p class="mt-1 text-sm text-[#8993A4]">{{ team.country }}</p>
        <p class="mt-4 text-sm text-[#B7FF3C]">
          FIDS Power {{ team.power }}
        </p>
      </RouterLink>
    </div>
  </section>
</template>

<script setup lang="ts">
import PageHeader from '@/components/common/SectionTitle.vue'

const teams = [
  { id: 'ahly', name: 'Al Ahly', short: 'AH', country: 'Egypt', power: 91 },
  { id: 'zamalek', name: 'Zamalek', short: 'ZA', country: 'Egypt', power: 84 },
  { id: 'pyramids', name: 'Pyramids FC', short: 'PY', country: 'Egypt', power: 82 },
  { id: 'liverpool', name: 'Liverpool', short: 'LIV', country: 'England', power: 94 },
  { id: 'arsenal', name: 'Arsenal', short: 'ARS', country: 'England', power: 92 },
  { id: 'barcelona', name: 'Barcelona', short: 'BAR', country: 'Spain', power: 93 },
  { id: 'realmadrid', name: 'Real Madrid', short: 'RM', country: 'Spain', power: 96 },
  { id: 'bayern', name: 'Bayern Munich', short: 'BM', country: 'Germany', power: 94 },
]
</script>
EOF
