<script setup lang="ts">
import { ref } from 'vue'
import { RouterLink } from 'vue-router'
import { MailCheck } from 'lucide-vue-next'

const message = ref('')
const error = ref('')

function resendVerification() {
  message.value = ''
  error.value = 'Email verification is not configured on the server yet.'
}
</script>

<template>
  <main class="flex min-h-[calc(100vh-64px)] items-center justify-center bg-[#070A0F] px-4 py-12 text-[#F5F7FA]">
    <div class="w-full max-w-md rounded-3xl border border-[#202936] bg-[#0F141C] p-6 text-center shadow-2xl sm:p-8">
      <div class="mx-auto mb-6 flex h-16 w-16 items-center justify-center rounded-2xl bg-blue-600/15 text-blue-400">
        <MailCheck class="h-8 w-8" />
      </div>

      <h1 class="text-2xl font-bold">Verify your email</h1>

      <p class="mt-3 text-sm leading-6 text-slate-400">
        Email verification is not yet configured for this application.
        You can sign in if your account is ready to use.
      </p>

      <div v-if="error" role="alert" class="mt-5 rounded-xl border border-amber-500/30 bg-amber-500/10 p-3 text-sm text-amber-200">
        {{ error }}
      </div>

      <div v-if="message" role="status" class="mt-5 text-sm text-emerald-300">
        {{ message }}
      </div>

      <button
        type="button"
        class="mt-6 w-full rounded-xl border border-[#293342] px-4 py-3 font-medium transition hover:bg-white/5"
        @click="resendVerification"
      >
        Resend verification email
      </button>

      <RouterLink to="/auth/login" class="mt-5 block text-sm font-semibold text-blue-400 hover:text-blue-300">
        Back to login
      </RouterLink>
    </div>
  </main>
</template>