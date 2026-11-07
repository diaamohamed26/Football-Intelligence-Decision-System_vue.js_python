<script setup lang="ts">
import { ref } from 'vue'

const name = ref('FIDS User')
const email = ref('user@example.com')
</script>

<template>
  <main class="min-h-[calc(100vh-64px)] bg-[#070A0F] px-4 py-12 text-[#F5F7FA]">
    <div class="mx-auto max-w-4xl">

      <div class="mb-8">
        <p class="text-xs font-bold uppercase tracking-[0.2em] text-[#B7FF3C]">
          Account
        </p>

        <h1 class="mt-2 text-3xl font-black">
          My Profile
        </h1>
      </div>

      <div class="rounded-3xl border border-[#202936] bg-[#0F141C] p-6 sm:p-8">
        <div class="flex flex-col gap-6 sm:flex-row sm:items-center">

          <div class="flex h-20 w-20 shrink-0 items-center justify-center rounded-2xl bg-[#B7FF3C] text-2xl font-black text-[#070A0F]">
            F
          </div>

          <div>
            <h2 class="text-xl font-bold">
              {{ name }}
            </h2>

            <p class="mt-1 text-sm text-[#8993A4]">
              {{ email }}
            </p>
          </div>
        </div>

        <div class="mt-8 grid gap-5 sm:grid-cols-2">
          <div>
            <label class="mb-2 block text-sm font-medium">
              Name
            </label>

            <input
              v-model="name"
              class="w-full rounded-xl border border-[#202936] bg-[#070A0F] px-4 py-3 text-sm outline-none focus:border-[#B7FF3C]"
            />
          </div>

          <div>
            <label class="mb-2 block text-sm font-medium">
              Email
            </label>

            <input
              v-model="email"
              type="email"
              class="w-full rounded-xl border border-[#202936] bg-[#070A0F] px-4 py-3 text-sm outline-none focus:border-[#B7FF3C]"
            />
          </div>
        </div>

        <button
          type="button"
          class="mt-6 rounded-xl bg-[#B7FF3C] px-5 py-3 text-sm font-bold text-[#070A0F]"
        >
          Save changes
        </button>
      </div>
    </div>
  </main>
</template>