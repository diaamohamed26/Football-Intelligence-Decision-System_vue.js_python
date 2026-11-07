<script setup lang="ts">
import { ref } from 'vue'
import { RouterLink } from 'vue-router'
import { ArrowLeft, Mail } from 'lucide-vue-next'

const email = ref('')
const message = ref('')
const error = ref('')

function handleSubmit() {
  message.value = ''
  error.value = 'Password reset is not configured on the server yet. Please contact the administrator.'
}
</script>

<template>
  <main class="min-h-[calc(100vh-64px)] bg-[#070A0F] px-4 py-12 text-[#F5F7FA]">
    <div class="mx-auto max-w-md rounded-3xl border border-[#202936] bg-[#0F141C] p-6 shadow-2xl sm:p-8">
      <RouterLink to="/auth/login" class="mb-8 inline-flex items-center gap-2 text-sm text-slate-400 hover:text-white">
        <ArrowLeft class="h-4 w-4" />
        Back to login
      </RouterLink>

      <div class="mb-6 flex h-12 w-12 items-center justify-center rounded-xl bg-blue-600/15 text-blue-400">
        <Mail class="h-6 w-6" />
      </div>

      <h1 class="text-2xl font-bold">Forgot password?</h1>
      <p class="mt-2 text-sm leading-6 text-slate-400">
        Enter your email address to request a password reset.
      </p>

      <div v-if="error" role="alert" class="mt-5 rounded-xl border border-amber-500/30 bg-amber-500/10 p-3 text-sm text-amber-200">
        {{ error }}
      </div>

      <div v-if="message" role="status" class="mt-5 rounded-xl border border-emerald-500/30 bg-emerald-500/10 p-3 text-sm text-emerald-300">
        {{ message }}
      </div>

      <form class="mt-8 space-y-5" @submit.prevent="handleSubmit">
        <div>
          <label for="email" class="mb-2 block text-sm font-medium">Email address</label>
          <input
            id="email"
            v-model="email"
            type="email"
            autocomplete="email"
            required
            placeholder="you@example.com"
            class="w-full rounded-xl border border-[#293342] bg-[#090D13] px-4 py-3 outline-none focus:border-blue-500"
          />
        </div>

        <button type="submit" class="w-full rounded-xl bg-blue-600 px-4 py-3 font-semibold hover:bg-blue-500">
          Request reset link
        </button>
      </form>
    </div>
  </main>
</template>