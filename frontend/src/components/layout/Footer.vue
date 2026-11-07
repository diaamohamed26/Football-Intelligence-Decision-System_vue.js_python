<script setup lang="ts">
import { RouterLink } from 'vue-router'
import {
  Zap,
  Github,
  Instagram,
  Linkedin
} from 'lucide-vue-next'
</script>

<template>
  <footer class="border-t border-[#202936] bg-[#070A0F]">
    <div class="mx-auto max-w-[1500px] px-4 py-12 sm:px-6 lg:px-8">

      <div class="grid gap-10 md:grid-cols-4">

        <!-- Brand -->
        <div class="md:col-span-2">
          <div class="flex items-center gap-3">
            <div
              class="flex h-10 w-10 items-center justify-center rounded-xl bg-[#B7FF3C] text-[#070A0F]"
            >
              <Zap :size="20" />
            </div>

            <div>
              <div class="text-xl font-black">FIDS</div>
              <div class="text-[9px] uppercase tracking-[0.25em] text-[#8993A4]">
                Football Intelligence
              </div>
            </div>
          </div>

          <p class="mt-5 max-w-md text-sm leading-7 text-[#8993A4]">
            Football intelligence platform built to understand the game
            beyond the score.
          </p>

          <div class="mt-6 flex gap-2">
            <a
              href="#"
              class="flex h-10 w-10 items-center justify-center rounded-xl border border-[#202936] text-[#8993A4] hover:text-white"
            >
              <Github :size="17" />
            </a>

            <a
              href="#"
              class="flex h-10 w-10 items-center justify-center rounded-xl border border-[#202936] text-[#8993A4] hover:text-white"
            >
              <Instagram :size="17" />
            </a>

            <a
              href="#"
              class="flex h-10 w-10 items-center justify-center rounded-xl border border-[#202936] text-[#8993A4] hover:text-white"
            >
              <Linkedin :size="17" />
            </a>
          </div>
        </div>

        <!-- Platform -->
        <div>
          <h3 class="text-sm font-bold text-white">
            Platform
          </h3>

          <div class="mt-4 flex flex-col gap-3 text-sm text-[#8993A4]">
            <RouterLink to="/matches" class="hover:text-[#B7FF3C]">
              Matches
            </RouterLink>

            <RouterLink to="/teams" class="hover:text-[#B7FF3C]">
              Teams
            </RouterLink>

            <RouterLink to="/players" class="hover:text-[#B7FF3C]">
              Players
            </RouterLink>

            <RouterLink to="/intelligence" class="hover:text-[#B7FF3C]">
              Intelligence
            </RouterLink>

            <RouterLink to="/scouting" class="hover:text-[#B7FF3C]">
              Scouting
            </RouterLink>
          </div>
        </div>

        <!-- Company -->
        <div>
          <h3 class="text-sm font-bold text-white">
            FIDS
          </h3>

          <div class="mt-4 flex flex-col gap-3 text-sm text-[#8993A4]">
            <RouterLink to="/news" class="hover:text-[#B7FF3C]">
              News
            </RouterLink>

            <RouterLink to="/ai" class="hover:text-[#B7FF3C]">
              FIDS AI
            </RouterLink>

            <RouterLink to="/auth/login" class="hover:text-[#B7FF3C]">
              Login
            </RouterLink>

            <RouterLink to="/auth/register" class="hover:text-[#B7FF3C]">
              Create Account
            </RouterLink>
          </div>
        </div>
      </div>

      <div class="mt-12 border-t border-[#202936] pt-6">
        <p class="text-center text-xs text-[#8993A4]">
          © {{ new Date().getFullYear() }} FIDS. Football Intelligence Decision System.
        </p>
      </div>
    </div>
  </footer>
</template>