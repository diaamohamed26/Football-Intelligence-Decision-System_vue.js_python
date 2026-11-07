<script setup lang="ts">
withDefaults(
  defineProps<{
    variant?: 'primary' | 'secondary' | 'ghost' | 'danger'
    type?: 'button' | 'submit'
    disabled?: boolean
  }>(),
  {
    variant: 'primary',
    type: 'button',
    disabled: false
  }
)
</script>

<template>
  <button
    :type="type"
    :disabled="disabled"
    class="inline-flex items-center justify-center gap-2 rounded-xl px-5 py-3 text-sm font-bold transition duration-200 disabled:cursor-not-allowed disabled:opacity-50"
    :class="{
      'bg-[#B7FF3C] text-[#070A0F] hover:scale-[1.02]':
        variant === 'primary',

      'border border-[#202936] bg-[#0F141C] text-white hover:border-[#B7FF3C]/50':
        variant === 'secondary',

      'text-[#8993A4] hover:bg-[#0F141C] hover:text-white':
        variant === 'ghost',

      'bg-[#FF4D67] text-white hover:opacity-90':
        variant === 'danger'
    }"
  >
    <slot />
  </button>
</template>