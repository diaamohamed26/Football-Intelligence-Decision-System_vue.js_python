cat > src/views/MatchDetails.vue <<'EOF'
<template>
  <section class="mx-auto max-w-6xl px-4 py-12">
    <div class="rounded-3xl border border-[#202936] bg-[#0F141C] p-8 text-center">
      <p class="text-sm text-[#B7FF3C]">Egyptian Premier League</p>

      <div class="mt-8 grid grid-cols-3 items-center gap-4">
        <div>
          <div class="mx-auto flex h-20 w-20 items-center justify-center rounded-full bg-[#151C26] text-2xl">
            A
          </div>
          <h2 class="mt-4 text-xl font-bold">Al Ahly</h2>
        </div>

        <div>
          <div class="text-5xl font-bold">2 - 1</div>
          <p class="mt-2 text-sm text-[#8993A4]">Full Time</p>
        </div>

        <div>
          <div class="mx-auto flex h-20 w-20 items-center justify-center rounded-full bg-[#151C26] text-2xl">
            Z
          </div>
          <h2 class="mt-4 text-xl font-bold">Zamalek</h2>
        </div>
      </div>
    </div>

    <div class="mt-6 grid gap-4 md:grid-cols-3">
      <Metric title="FIDS Rating" value="82" />
      <Metric title="xG" value="1.84" />
      <Metric title="Possession" value="58%" />
    </div>
  </section>
</template>

<script setup lang="ts">
import { defineComponent, h } from 'vue'

const Metric = defineComponent({
  props: {
    title: String,
    value: String,
  },
  setup(props) {
    return () =>
      h('div', { class: 'rounded-2xl border border-[#202936] bg-[#0F141C] p-6' }, [
        h('p', { class: 'text-sm text-[#8993A4]' }, props.title),
        h('p', { class: 'mt-2 text-3xl font-bold' }, props.value),
      ])
  },
})
</script>
EOF