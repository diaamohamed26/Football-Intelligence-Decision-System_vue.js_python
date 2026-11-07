<template>
  <div
    class="relative isolate min-h-screen overflow-hidden bg-[#070a09] font-sans text-white"
  >
    <!-- Background effects -->
    <div class="pointer-events-none absolute inset-0 -z-10 overflow-hidden">
      <div
        class="absolute -left-32 -top-48 h-[420px] w-[420px] rounded-full bg-lime-400/15 blur-[120px]"
      ></div>

      <div
        class="absolute -bottom-40 -right-40 h-[420px] w-[420px] rounded-full bg-emerald-600/10 blur-[120px]"
      ></div>

      <div
        class="absolute inset-0 bg-[linear-gradient(rgba(255,255,255,0.025)_1px,transparent_1px),linear-gradient(90deg,rgba(255,255,255,0.025)_1px,transparent_1px)] bg-[size:48px_48px] opacity-50"
      ></div>
    </div>

    <!-- Header -->
    <header
      class="relative z-10 mx-auto flex w-[calc(100%-32px)] max-w-6xl items-center justify-between border-b border-white/[0.08] py-5 sm:w-[calc(100%-48px)] sm:py-6"
    >
      <RouterLink to="/" class="group flex items-center gap-3">
        <span
          class="grid h-10 w-10 place-items-center rounded-xl bg-lime-300 text-xl font-black text-[#10150b] transition-transform group-hover:scale-105 sm:h-11 sm:w-11"
        >
          F
        </span>

        <span class="flex flex-col gap-0.5">
          <span class="text-xl font-extrabold tracking-wider">FIDS</span>
          <span
            class="text-[8px] font-semibold tracking-[1.5px] text-zinc-500 sm:text-[9px]"
          >
            FOOTBALL INTELLIGENCE
          </span>
        </span>
      </RouterLink>

      <RouterLink
        to="/"
        class="flex items-center gap-2 text-xs text-zinc-400 transition-colors hover:text-lime-300 sm:text-sm"
      >
        <span class="text-lg" aria-hidden="true">←</span>
        <span>Back to Home</span>
      </RouterLink>
    </header>

    <!-- Main -->
    <main class="mx-auto w-full max-w-lg px-4 pb-8 pt-10 sm:px-6 sm:pt-14">
      <!-- Intro -->
      <section class="text-center">
        <div
          class="inline-flex items-center gap-2 text-[9px] font-bold tracking-[2px] text-lime-300 sm:text-[10px]"
        >
          <span
            class="h-1.5 w-1.5 rounded-full bg-lime-300 shadow-[0_0_12px_rgba(190,242,100,0.7)]"
          ></span>
          FOOTBALL INTELLIGENCE PLATFORM
        </div>

        <h1
          class="mt-5 text-4xl font-black leading-tight tracking-[-1.5px] sm:text-5xl"
        >
          See the game
          <span class="block text-lime-300">differently.</span>
        </h1>

        <p
          class="mx-auto mt-4 max-w-md text-sm leading-7 text-zinc-400 sm:text-[15px]"
        >
          Access football insights, match intelligence, player analytics, and
          scouting tools — all in one place.
        </p>
      </section>

      <!-- Features -->
      <section class="mt-8 space-y-4">
        <div class="flex items-center gap-3.5">
          <div
            class="grid h-11 w-11 shrink-0 place-items-center rounded-xl border border-lime-300/15 bg-lime-300/[0.06] text-xl text-lime-300"
            aria-hidden="true"
          >
            ↗
          </div>

          <div>
            <h2 class="text-sm font-bold text-zinc-100">
              Match Intelligence
            </h2>
            <p class="mt-1 text-xs leading-5 text-zinc-500">
              Explore matches with meaningful insights.
            </p>
          </div>
        </div>

        <div class="flex items-center gap-3.5">
          <div
            class="grid h-11 w-11 shrink-0 place-items-center rounded-xl border border-lime-300/15 bg-lime-300/[0.06] text-xl text-lime-300"
            aria-hidden="true"
          >
            ◎
          </div>

          <div>
            <h2 class="text-sm font-bold text-zinc-100">Player Scouting</h2>
            <p class="mt-1 text-xs leading-5 text-zinc-500">
              Discover talent and analyze performance.
            </p>
          </div>
        </div>

        <div class="flex items-center gap-3.5">
          <div
            class="grid h-11 w-11 shrink-0 place-items-center rounded-xl border border-lime-300/15 bg-lime-300/[0.06] text-xl text-lime-300"
            aria-hidden="true"
          >
            ⌁
          </div>

          <div>
            <h2 class="text-sm font-bold text-zinc-100">
              AI-Powered Analysis
            </h2>
            <p class="mt-1 text-xs leading-5 text-zinc-500">
              Turn football data into better decisions.
            </p>
          </div>
        </div>
      </section>

      <!-- Login / Register content -->
      <section
        class="mt-8 rounded-2xl border border-white/[0.09] bg-[#0f1310]/90 p-5 shadow-2xl shadow-black/20 backdrop-blur-xl sm:p-7"
      >
        <RouterView />
      </section>

      <!-- Footer -->
      <footer
        class="mt-7 text-center text-[9px] font-semibold tracking-[1.5px] text-zinc-600"
      >
        BUILT FOR THE LOVE OF THE GAME
        <span class="px-1.5 text-lime-300">·</span>
        FIDS © {{ currentYear }}
      </footer>
    </main>
  </div>
</template>

<script setup lang="ts">
import { RouterLink, RouterView } from 'vue-router'

const currentYear = new Date().getFullYear()
</script>
