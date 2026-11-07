cat > src/views/Players.vue <<'EOF'
<template>
  <section class="mx-auto max-w-7xl px-4 py-12">
    <PageHeader title="Players" subtitle="Explore player profiles, ratings and performance DNA." />

    <div class="mb-8">
      <input
        placeholder="Search players..."
        class="w-full rounded-xl border border-[#202936] bg-[#0F141C] px-4 py-3 outline-none focus:border-[#B7FF3C]"
      />
    </div>

    <div class="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
      <RouterLink
        v-for="player in players"
        :key="player.id"
        :to="`/players/${player.id}`"
        class="rounded-2xl border border-[#202936] bg-[#0F141C] p-6 hover:border-[#B7FF3C]"
      >
        <div class="flex h-20 w-20 items-center justify-center rounded-full bg-[#151C26] text-2xl font-bold">
          {{ player.number }}
        </div>

        <h2 class="mt-5 text-lg font-bold">{{ player.name }}</h2>
        <p class="text-sm text-[#8993A4]">{{ player.position }}</p>

        <div class="mt-5 flex items-center justify-between">
          <span class="text-xs text-[#8993A4]">FIDS Rating</span>
          <span class="font-bold text-[#B7FF3C]">{{ player.rating }}</span>
        </div>
      </RouterLink>
    </div>
  </section>
</template>

<script setup lang="ts">
import PageHeader from '@/components/common/SectionTitle.vue'

const players = [
  { id: 'salah', name: 'Mohamed Salah', position: 'RW', number: '11', rating: 94 },
  { id: 'omar-marmoush', name: 'Omar Marmoush', position: 'FW', number: '7', rating: 88 },
  { id: 'tr', name: 'Trent Alexander-Arnold', position: 'RB', number: '66', rating: 91 },
  { id: 'saka', name: 'Bukayo Saka', position: 'RW', number: '7', rating: 90 },
  { id: 'pedri', name: 'Pedri', position: 'CM', number: '8', rating: 92 },
  { id: 'bellingham', name: 'Jude Bellingham', position: 'CM', number: '5', rating: 93 },
  { id: 'vinicius', name: 'Vinicius Jr.', position: 'LW', number: '7', rating: 94 },
  { id: 'musiala', name: 'Jamal Musiala', position: 'AM', number: '10', rating: 91 },
]
</script>
EOF