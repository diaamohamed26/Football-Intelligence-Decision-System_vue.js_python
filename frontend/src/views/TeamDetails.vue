cat > src/views/TeamDetails.vue <<'EOF'
<template>
  <section class="mx-auto max-w-7xl px-4 py-12">
    <div class="rounded-3xl border border-[#202936] bg-[#0F141C] p-8">
      <div class="flex flex-col gap-6 sm:flex-row sm:items-center">
        <div class="flex h-24 w-24 items-center justify-center rounded-full bg-[#151C26] text-2xl font-bold">
          AH
        </div>

        <div>
          <p class="text-sm text-[#B7FF3C]">Egypt</p>
          <h1 class="mt-1 text-4xl font-bold">Al Ahly</h1>
          <p class="mt-2 text-[#8993A4]">Egyptian Premier League</p>
        </div>
      </div>
    </div>

    <div class="mt-6 grid gap-4 md:grid-cols-4">
      <Metric title="Team Power" value="91" />
      <Metric title="Momentum" value="+8.4" />
      <Metric title="Tactical Stability" value="87" />
      <Metric title="Creation Index" value="84" />
    </div>
  </section>
</template>

<script setup lang="ts">
import { defineComponent, h } from 'vue'

const Metric = defineComponent({
  props: { title: String, value: String },
  setup(props) {
    return () =>
      h('div', { class: 'rounded-2xl border border-[#202936] bg-[#0F141C] p-6' }, [
        h('p', { class: 'text-sm text-[#8993A4]' }, props.title),
        h('p', { class: 'mt-2 text-3xl font-bold text-[#B7FF3C]' }, props.value),
      ])
  },
})
</script>
EOF