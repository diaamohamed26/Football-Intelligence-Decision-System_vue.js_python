cat > src/views/Scouting.vue <<'EOF'
<template>
  <section class="mx-auto max-w-7xl px-4 py-12">
    <PageHeader title="AI Scouting" subtitle="Find players by profile, role, age and tactical fit." />

    <div class="grid gap-6 lg:grid-cols-3">
      <div class="rounded-2xl border border-[#202936] bg-[#0F141C] p-6">
        <h2 class="text-lg font-bold">Scout Filters</h2>

        <div class="mt-6 space-y-4">
          <input
            placeholder="Position"
            class="w-full rounded-xl border border-[#202936] bg-[#070A0F] px-4 py-3"
          />

          <input
            placeholder="Maximum age"
            class="w-full rounded-xl border border-[#202936] bg-[#070A0F] px-4 py-3"
          />

          <input
            placeholder="Budget"
            class="w-full rounded-xl border border-[#202936] bg-[#070A0F] px-4 py-3"
          />

          <button class="w-full rounded-xl bg-[#B7FF3C] px-4 py-3 font-semibold text-[#070A0F]">
            Find Players
          </button>
        </div>
      </div>

      <div class="lg:col-span-2">
        <div class="grid gap-4 sm:grid-cols-2">
          <div
            v-for="player in players"
            :key="player.name"
            class="rounded-2xl border border-[#202936] bg-[#0F141C] p-6"
          >
            <p class="text-xs text-[#B7FF3C]">MATCHED PROFILE</p>
            <h3 class="mt-3 font-bold">{{ player.name }}</h3>
            <p class="mt-1 text-sm text-[#8993A4]">{{ player.position }}</p>
            <div class="mt-5 flex justify-between text-sm">
              <span class="text-[#8993A4]">Fit</span>
              <strong>{{ player.fit }}%</strong>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import PageHeader from '@/components/common/SectionTitle.vue'

const players = [
  { name: 'Rising Talent A', position: 'Central Midfielder', fit: 94 },
  { name: 'Rising Talent B', position: 'Right Winger', fit: 91 },
  { name: 'Rising Talent C', position: 'Centre Back', fit: 88 },
  { name: 'Rising Talent D', position: 'Striker', fit: 86 },
]
</script>
EOF