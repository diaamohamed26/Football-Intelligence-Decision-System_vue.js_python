<script setup lang="ts">
import { ref } from 'vue'
import { Bot, Send, Sparkles } from 'lucide-vue-next'

const question = ref('')

const suggestions = [
  'Compare Al Ahly and Zamalek',
  'Find the best young Egyptian players',
  'Analyze the latest Liverpool match'
]
</script>

<template>
  <section
    class="relative overflow-hidden rounded-3xl border border-[#B7FF3C]/20 bg-[#0F141C] p-6 sm:p-8"
  >
    <div
      class="pointer-events-none absolute -right-20 -top-20 h-60 w-60 rounded-full bg-[#B7FF3C]/5 blur-3xl"
    />

    <div class="relative">

      <div class="flex items-center gap-3">
        <div
          class="flex h-11 w-11 items-center justify-center rounded-xl bg-[#B7FF3C]/10 text-[#B7FF3C]"
        >
          <Bot :size="22" />
        </div>

        <div>
          <div class="flex items-center gap-2">
            <h2 class="text-lg font-black">
              FIDS AI
            </h2>

            <Sparkles
              :size="15"
              class="text-[#B7FF3C]"
            />
          </div>

          <p class="text-xs text-[#8993A4]">
            Your football intelligence assistant
          </p>
        </div>
      </div>

      <div class="mt-6">
        <h3 class="text-2xl font-black sm:text-3xl">
          Ask anything about football.
        </h3>

        <p class="mt-2 max-w-xl text-sm leading-6 text-[#8993A4]">
          Analyze matches, compare players, discover talent and understand
          tactical decisions.
        </p>
      </div>

      <div class="mt-6 flex flex-wrap gap-2">
        <button
          v-for="suggestion in suggestions"
          :key="suggestion"
          class="rounded-full border border-[#202936] bg-[#070A0F] px-3 py-2 text-xs text-[#8993A4] transition hover:border-[#B7FF3C]/30 hover:text-white"
          @click="question = suggestion"
        >
          {{ suggestion }}
        </button>
      </div>

      <div
        class="mt-5 flex items-center rounded-2xl border border-[#202936] bg-[#070A0F] p-2 focus-within:border-[#B7FF3C]/40"
      >
        <input
          v-model="question"
          type="text"
          placeholder="Ask FIDS AI..."
          class="min-w-0 flex-1 bg-transparent px-4 py-3 text-sm text-white outline-none placeholder:text-[#8993A4]"
        />

        <button
          class="flex h-11 w-11 shrink-0 items-center justify-center rounded-xl bg-[#B7FF3C] text-[#070A0F] transition hover:scale-105"
        >
          <Send :size="18" />
        </button>
      </div>

    </div>
  </section>
</template>