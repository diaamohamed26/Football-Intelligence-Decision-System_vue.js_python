<script setup lang="ts">
import { ref } from 'vue'

const notifications = ref(true)
const matchAlerts = ref(true)
const darkMode = ref(true)
</script>

<template>
  <main class="min-h-[calc(100vh-64px)] bg-[#070A0F] px-4 py-12 text-[#F5F7FA]">
    <div class="mx-auto max-w-4xl">

      <p class="text-xs font-bold uppercase tracking-[0.2em] text-[#B7FF3C]">
        Account
      </p>

      <h1 class="mt-2 text-3xl font-black">
        Settings
      </h1>

      <div class="mt-8 overflow-hidden rounded-3xl border border-[#202936] bg-[#0F141C]">

        <label class="flex items-center justify-between border-b border-[#202936] p-6">
          <div>
            <p class="font-semibold">Notifications</p>
            <p class="mt-1 text-sm text-[#8993A4]">
              Receive FIDS notifications.
            </p>
          </div>

          <input
            v-model="notifications"
            type="checkbox"
            class="h-5 w-5 accent-[#B7FF3C]"
          />
        </label>

        <label class="flex items-center justify-between border-b border-[#202936] p-6">
          <div>
            <p class="font-semibold">Match alerts</p>
            <p class="mt-1 text-sm text-[#8993A4]">
              Get notified about important matches.
            </p>
          </div>

          <input
            v-model="matchAlerts"
            type="checkbox"
            class="h-5 w-5 accent-[#B7FF3C]"
          />
        </label>

        <label class="flex items-center justify-between p-6">
          <div>
            <p class="font-semibold">Dark mode</p>
            <p class="mt-1 text-sm text-[#8993A4]">
              Use the FIDS dark interface.
            </p>
          </div>

          <input
            v-model="darkMode"
            type="checkbox"
            class="h-5 w-5 accent-[#B7FF3C]"
          />
        </label>

      </div>
    </div>
  </main>
</template>