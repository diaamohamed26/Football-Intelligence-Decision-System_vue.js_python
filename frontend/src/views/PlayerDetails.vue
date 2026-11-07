cat > src/views/PlayerDetails.vue <<'EOF'
<template>
  <section class="mx-auto max-w-7xl px-4 py-12">
    <div class="rounded-3xl border border-[#202936] bg-[#0F141C] p-8">
      <div class="flex flex-col gap-6 sm:flex-row sm:items-center">
        <div class="flex h-28 w-28 items-center justify-center rounded-full bg-[#151C26] text-3xl font-bold">
          11
        </div>

        <div>
          <p class="text-sm text-[#B7FF3C]">Forward · RW</p>
          <h1 class="mt-2 text-4xl font-bold">Mohamed Salah</h1>
          <p class="mt-2 text-[#8993A4]">Egypt</p>
        </div>

        <div class="sm:ml-auto">
          <p class="text-sm text-[#8993A4]">FIDS Rating</p>
          <p class="text-5xl font-bold text-[#B7FF3C]">94</p>
        </div>
      </div>
    </div>

    <div class="mt-6 grid gap-4 md:grid-cols-3">
      <div
        v-for="metric in metrics"
        :key="metric.name"
        class="rounded-2xl border border-[#202936] bg-[#0F141C] p-6"
      >
        <p class="text-sm text-[#8993A4]">{{ metric.name }}</p>
        <p class="mt-2 text-3xl font-bold">{{ metric.value }}</p>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
const metrics = [
  { name: 'Finisher', value: '96' },
  { name: 'Creator', value: '91' },
  { name: 'Carrier', value: '89' },
  { name: 'Progressor', value: '88' },
  { name: 'Presser', value: '82' },
  { name: 'Dueler', value: '76' },
]
</script>
EOF