cat > src/views/Intelligence.vue <<'EOF'
<template>
  <section class="mx-auto max-w-7xl px-4 py-12">
    <PageHeader title="Intelligence" subtitle="Advanced football metrics and decision intelligence." />

    <div class="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
      <div
        v-for="item in intelligence"
        :key="item.title"
        class="rounded-2xl border border-[#202936] bg-[#0F141C] p-6"
      >
        <div class="text-sm text-[#B7FF3C]">FIDS METRIC</div>
        <h2 class="mt-3 text-xl font-bold">{{ item.title }}</h2>
        <p class="mt-2 text-sm leading-6 text-[#8993A4]">
          {{ item.description }}
        </p>
        <div class="mt-6 text-4xl font-bold">{{ item.value }}</div>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import PageHeader from '@/components/common/SectionTitle.vue'

const intelligence = [
  { title: 'FIDS Rating', value: '94', description: 'Composite player intelligence rating.' },
  { title: 'Team Power', value: '91', description: 'Team-level strength across multiple dimensions.' },
  { title: 'Momentum', value: '+8.4', description: 'Recent performance trajectory.' },
  { title: 'Tactical Stability', value: '87', description: 'Consistency of tactical behavior.' },
  { title: 'Transition Efficiency', value: '82', description: 'Efficiency during attacking and defensive transitions.' },
  { title: 'Creation Index', value: '89', description: 'Chance creation and progression intelligence.' },
]
</script>
EOF