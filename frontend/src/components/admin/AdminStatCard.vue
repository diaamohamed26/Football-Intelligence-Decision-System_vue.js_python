<template>
  <div
    class="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm transition hover:shadow-md"
  >
    <div class="flex items-start justify-between">
      <div
        class="flex h-11 w-11 items-center justify-center rounded-xl bg-blue-50 text-xl"
      >
        {{ icon }}
      </div>

      <span
        class="rounded-full bg-emerald-50 px-2 py-1 text-xs font-semibold text-emerald-600"
      >
        {{ change }}
      </span>
    </div>

    <p class="mt-5 text-sm text-slate-500">
      {{ title }}
    </p>

    <h3 class="mt-1 text-2xl font-bold text-slate-900">
      {{ value }}
    </h3>

    <p class="mt-1 text-xs text-slate-400">
      {{ description }}
    </p>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  title: string
  value: string | number
  icon: string
  change: string
  description: string
}>()
</script>