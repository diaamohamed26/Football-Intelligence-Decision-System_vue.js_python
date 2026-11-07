<script setup lang="ts">
import type { Component } from 'vue'

defineProps<{
  label: string
  value: string | number
  change?: string
  icon?: Component
}>()
</script>

<template>
  <div
    class="rounded-2xl border border-[#202936] bg-[#0F141C] p-5 transition hover:-translate-y-0.5 hover:border-[#B7FF3C]/20"
  >
    <div class="flex items-start justify-between">

      <div>
        <p class="text-xs font-medium uppercase tracking-wider text-[#8993A4]">
          {{ label }}
        </p>

        <p class="mt-3 text-2xl font-black text-white">
          {{ value }}
        </p>
      </div>

      <div
        v-if="icon"
        class="flex h-10 w-10 items-center justify-center rounded-xl bg-[#B7FF3C]/10 text-[#B7FF3C]"
      >
        <component :is="icon" :size="19" />
      </div>
    </div>

    <p
      v-if="change"
      class="mt-3 text-xs font-semibold text-[#B7FF3C]"
    >
      {{ change }}
    </p>
  </div>
</template>