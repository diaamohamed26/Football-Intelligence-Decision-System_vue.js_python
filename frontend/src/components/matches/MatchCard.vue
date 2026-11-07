<script setup lang="ts">
import { RouterLink } from 'vue-router'
import { ArrowRight } from 'lucide-vue-next'

interface Match {
  id: string
  homeTeam: string
  awayTeam: string
  homeScore: number | null
  awayScore: number | null
  time: string
  status: string
  competition: string
}

defineProps<{
  match: Match
}>()
</script>

<template>
  <RouterLink
    :to="`/matches/${match.id}`"
    class="group block rounded-2xl border border-[#202936] bg-[#0F141C] p-5 transition duration-300 hover:border-[#B7FF3C]/40 hover:bg-[#151C26]"
  >
    <!-- Competition -->
    <div class="mb-5 flex items-center justify-between">
      <span class="text-xs font-medium text-[#8993A4]">
        {{ match.competition }}
      </span>

      <span
        class="rounded-full px-2.5 py-1 text-[10px] font-bold uppercase tracking-wider"
        :class="
          match.status === 'LIVE'
            ? 'bg-[#FF4D67]/10 text-[#FF4D67]'
            : 'bg-[#202936] text-[#8993A4]'
        "
      >
        {{ match.status }}
      </span>
    </div>

    <!-- Teams -->
    <div class="grid grid-cols-[1fr_auto_1fr] items-center gap-4">

      <!-- Home -->
      <div class="min-w-0">
        <p class="truncate text-sm font-semibold text-[#F5F7FA]">
          {{ match.homeTeam }}
        </p>

        <p class="mt-1 text-xs text-[#8993A4]">
          Home
        </p>
      </div>

      <!-- Score / Time -->
      <div class="text-center">
        <template v-if="match.status === 'Scheduled'">
          <p class="text-lg font-bold text-[#F5F7FA]">
            {{ match.time }}
          </p>
        </template>

        <template v-else>
          <div class="flex items-center gap-2 text-xl font-black">
            <span>{{ match.homeScore ?? '-' }}</span>
            <span class="text-[#8993A4]">:</span>
            <span>{{ match.awayScore ?? '-' }}</span>
          </div>
        </template>
      </div>

      <!-- Away -->
      <div class="min-w-0 text-right">
        <p class="truncate text-sm font-semibold text-[#F5F7FA]">
          {{ match.awayTeam }}
        </p>

        <p class="mt-1 text-xs text-[#8993A4]">
          Away
        </p>
      </div>
    </div>

    <!-- Footer -->
    <div class="mt-5 flex items-center justify-end border-t border-[#202936] pt-4">
      <span
        class="flex items-center gap-1 text-xs font-semibold text-[#8993A4] transition group-hover:text-[#B7FF3C]"
      >
        Match Center

        <ArrowRight
          class="h-3.5 w-3.5 transition-transform group-hover:translate-x-1"
        />
      </span>
    </div>
  </RouterLink>
</template>