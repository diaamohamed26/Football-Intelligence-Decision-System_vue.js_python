<script setup lang="ts">
defineProps<{
  modelValue: boolean
  title: string
  description: string
}>()

defineEmits<{
  'update:modelValue': [value: boolean]
}>()
</script>

<template>
  <div class="flex items-center justify-between gap-4 rounded-xl border border-slate-800 bg-[#090d16] p-4">
    <div class="min-w-0">
      <p class="text-sm font-medium text-slate-200">{{ title }}</p>
      <p class="mt-1 text-xs leading-5 text-slate-500">{{ description }}</p>
    </div>

    <button
      type="button"
      role="switch"
      :aria-checked="modelValue"
      :aria-label="title"
      @click="$emit('update:modelValue', !modelValue)"
      class="relative inline-flex h-6 w-11 shrink-0 items-center rounded-full transition-colors focus:outline-none focus:ring-2 focus:ring-cyan-400/50"
      :class="modelValue ? 'bg-cyan-400' : 'bg-slate-700'"
    >
      <span
        class="inline-block h-4 w-4 transform rounded-full bg-white shadow transition-transform"
        :class="modelValue ? 'translate-x-6' : 'translate-x-1'"
      ></span>
    </button>
  </div>
</template>
