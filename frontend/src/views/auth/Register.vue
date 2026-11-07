<script setup lang="ts">
import { ref } from 'vue'
import { useRouter, RouterLink } from 'vue-router'
import { ArrowRight, Mail, UserRound, LockKeyhole } from 'lucide-vue-next'
import api from '@/services/api'

const router = useRouter()

const name = ref('')
const email = ref('')
const password = ref('')
const confirmPassword = ref('')
const agree = ref(false)
const loading = ref(false)
const error = ref('')
const success = ref('')

async function handleRegister() {
  error.value = ''
  success.value = ''

  if (!name.value.trim() || !email.value.trim() || !password.value) {
    error.value = 'Please fill in all required fields.'
    return
  }

  if (password.value.length < 8) {
    error.value = 'Password must contain at least 8 characters.'
    return
  }

  if (password.value !== confirmPassword.value) {
    error.value = 'Passwords do not match.'
    return
  }

  if (!agree.value) {
    error.value = 'Please accept the Terms of Service and Privacy Policy.'
    return
  }

  const nameParts = name.value.trim().split(/\s+/)
  const firstName = nameParts.shift() || ''
  const lastName = nameParts.join(' ')

  loading.value = true

  try {
    await api.post('/auth/register/', {
      username: email.value.trim().toLowerCase(),
      email: email.value.trim().toLowerCase(),
      first_name: firstName,
      last_name: lastName,
      password: password.value,
    })

    success.value = 'Account created successfully. Please sign in.'

    await router.push({
      path: '/auth/login',
      query: { registered: 'true' },
    })
  } catch (err: any) {
    const data = err.response?.data

    if (data && typeof data === 'object') {
      const firstError = Object.values(data).flat()[0]
      error.value = typeof firstError === 'string'
        ? firstError
        : 'Registration failed. Please check your information.'
    } else {
      error.value = 'Unable to connect to the server. Please try again.'
    }
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <main class="min-h-[calc(100vh-64px)] bg-[#070A0F] px-4 py-12 text-[#F5F7FA]">
    <div class="mx-auto max-w-md">
      <div class="rounded-3xl border border-[#202936] bg-[#0F141C] p-6 shadow-2xl sm:p-8">
        <div class="mb-8 text-center">
          <div class="mx-auto mb-4 flex h-14 w-14 items-center justify-center rounded-2xl bg-blue-600 text-xl font-bold">
            F
          </div>
          <h1 class="text-2xl font-bold">Create your account</h1>
          <p class="mt-2 text-sm text-slate-400">
            Join FIDS and explore football intelligence.
          </p>
        </div>

        <div
          v-if="error"
          role="alert"
          class="mb-5 rounded-xl border border-red-500/30 bg-red-500/10 p-3 text-sm text-red-300"
        >
          {{ error }}
        </div>

        <div
          v-if="success"
          role="status"
          class="mb-5 rounded-xl border border-emerald-500/30 bg-emerald-500/10 p-3 text-sm text-emerald-300"
        >
          {{ success }}
        </div>

        <form class="space-y-5" @submit.prevent="handleRegister">
          <div>
            <label for="name" class="mb-2 block text-sm font-medium">Full name</label>
            <div class="relative">
              <UserRound class="absolute left-3 top-1/2 h-5 w-5 -translate-y-1/2 text-slate-500" />
              <input
                id="name"
                v-model="name"
                type="text"
                autocomplete="name"
                required
                placeholder="Your full name"
                class="w-full rounded-xl border border-[#293342] bg-[#090D13] py-3 pl-11 pr-4 outline-none transition focus:border-blue-500"
              />
            </div>
          </div>

          <div>
            <label for="email" class="mb-2 block text-sm font-medium">Email address</label>
            <div class="relative">
              <Mail class="absolute left-3 top-1/2 h-5 w-5 -translate-y-1/2 text-slate-500" />
              <input
                id="email"
                v-model="email"
                type="email"
                autocomplete="email"
                required
                placeholder="you@example.com"
                class="w-full rounded-xl border border-[#293342] bg-[#090D13] py-3 pl-11 pr-4 outline-none transition focus:border-blue-500"
              />
            </div>
          </div>

          <div>
            <label for="password" class="mb-2 block text-sm font-medium">Password</label>
            <div class="relative">
              <LockKeyhole class="absolute left-3 top-1/2 h-5 w-5 -translate-y-1/2 text-slate-500" />
              <input
                id="password"
                v-model="password"
                type="password"
                autocomplete="new-password"
                minlength="8"
                required
                placeholder="At least 8 characters"
                class="w-full rounded-xl border border-[#293342] bg-[#090D13] py-3 pl-11 pr-4 outline-none transition focus:border-blue-500"
              />
            </div>
          </div>

          <div>
            <label for="confirmPassword" class="mb-2 block text-sm font-medium">
              Confirm password
            </label>
            <input
              id="confirmPassword"
              v-model="confirmPassword"
              type="password"
              autocomplete="new-password"
              required
              placeholder="Repeat your password"
              class="w-full rounded-xl border border-[#293342] bg-[#090D13] px-4 py-3 outline-none transition focus:border-blue-500"
            />
          </div>

          <label class="flex items-start gap-3 text-sm text-slate-400">
            <input
              v-model="agree"
              type="checkbox"
              class="mt-1 accent-blue-600"
            />
            <span>I agree to the Terms of Service and Privacy Policy.</span>
          </label>

          <button
            type="submit"
            :disabled="loading"
            class="flex w-full items-center justify-center gap-2 rounded-xl bg-blue-600 px-4 py-3 font-semibold transition hover:bg-blue-500 disabled:cursor-not-allowed disabled:opacity-60"
          >
            {{ loading ? 'Creating account...' : 'Create account' }}
            <ArrowRight v-if="!loading" class="h-4 w-4" />
          </button>
        </form>

        <p class="mt-6 text-center text-sm text-slate-400">
          Already have an account?
          <RouterLink to="/auth/login" class="font-semibold text-blue-400 hover:text-blue-300">
            Sign in
          </RouterLink>
        </p>
      </div>
    </div>
  </main>
</template>