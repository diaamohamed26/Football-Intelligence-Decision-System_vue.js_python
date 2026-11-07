<script setup lang="ts">
defineProps<{
  title: string
  subtitle?: string
}>()
</script>

<template>
  <div class="mb-6 flex items-end justify-between gap-4">
    <div>
      <h2 class="text-xl font-black tracking-tight text-white sm:text-2xl">
        {{ title }}
      </h2>

      <p
        v-if="subtitle"
        class="mt-1 text-sm text-[#8993A4]"
      >
        {{ subtitle }}
      </p>
    </div>

    <slot name="action" />
  </div>
</template>