<template>
  <span
    class="inline-flex items-center gap-1.5 rounded-full px-2.5 py-1 text-xs font-semibold"
    :class="classes"
  >
    <span
      class="h-1.5 w-1.5 rounded-full"
      :class="dotClass"
    />

    {{ status }}
  </span>
</template>

<script setup lang="ts">
import { computed } from 'vue'

const props = defineProps<{
  status: 'active' | 'inactive' | 'pending'
}>()

const classes = computed(() => ({
  'bg-emerald-50 text-emerald-700': props.status === 'active',
  'bg-red-50 text-red-700': props.status === 'inactive',
  'bg-amber-50 text-amber-700': props.status === 'pending'
}))

const dotClass = computed(() => ({
  'bg-emerald-500': props.status === 'active',
  'bg-red-500': props.status === 'inactive',
  'bg-amber-500': props.status === 'pending'
}))
</script>