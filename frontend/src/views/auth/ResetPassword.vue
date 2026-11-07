<script setup lang="ts">
import { ref } from 'vue'
import { RouterLink } from 'vue-router'
import { LockKeyhole } from 'lucide-vue-next'

const password = ref('')
const confirmPassword = ref('')
const error = ref('')

function handleSubmit() {
  error.value = ''

  if (password.value.length < 8) {
    error.value = 'Password must contain at least 8 characters.'
    return
  }

  if (password.value !== confirmPassword.value) {
    error.value = 'Passwords do not match.'
    return
  }

  error.value = 'Password reset is not configured on the server yet.'
}
</script>

<template>
  <main class="min-h-[calc(100vh-64px)] bg-[#070A0F] px-4 py-12 text-[#F5F7FA]">
    <div class="mx-auto max-w-md rounded-3xl border border-[#202936] bg-[#0F141C] p-6 shadow-2xl sm:p-8">
      <div class="mb-6 flex h-12 w-12 items-center justify-center rounded-xl bg-blue-600/15 text-blue-400">
        <LockKeyhole class="h-6 w-6" />
      </div>

      <h1 class="text-2xl font-bold">Reset password</h1>
      <p class="mt-2 text-sm text-slate-400">Choose a new password for your account.</p>

      <div v-if="error" role="alert" class="mt-5 rounded-xl border border-amber-500/30 bg-amber-500/10 p-3 text-sm text-amber-200">
        {{ error }}
      </div>

      <form class="mt-8 space-y-5" @submit.prevent="handleSubmit">
        <div>
          <label for="password" class="mb-2 block text-sm font-medium">New password</label>
          <input
            id="password"
            v-model="password"
            type="password"
            autocomplete="new-password"
            minlength="8"
            required
            placeholder="At least 8 characters"
            class="w-full rounded-xl border border-[#293342] bg-[#090D13] px-4 py-3 outline-none focus:border-blue-500"
          />
        </div>

        <div>
          <label for="confirmPassword" class="mb-2 block text-sm font-medium">Confirm password</label>
          <input
            id="confirmPassword"
            v-model="confirmPassword"
            type="password"
            autocomplete="new-password"
            required
            placeholder="Repeat your password"
            class="w-full rounded-xl border border-[#293342] bg-[#090D13] px-4 py-3 outline-none focus:border-blue-500"
          />
        </div>

        <button type="submit" class="w-full rounded-xl bg-blue-600 px-4 py-3 font-semibold hover:bg-blue-500">
          Update password
        </button>
      </form>

      <RouterLink to="/auth/login" class="mt-6 block text-center text-sm text-blue-400 hover:text-blue-300">
        Back to login
      </RouterLink>
    </div>
  </main>
</template>