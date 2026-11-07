<script setup lang="ts">
import { ref } from 'vue'
import { useRoute, useRouter, RouterLink } from 'vue-router'
import { Mail, LockKeyhole, ArrowRight } from 'lucide-vue-next'
import api from '@/services/api'

interface LoginResponse {
  access: string
  refresh: string
  username: string
  email: string
  role?: string
  is_admin?: boolean
}

const router = useRouter()
const route = useRoute()

const email = ref('')
const password = ref('')
const loading = ref(false)
const error = ref('')
const success = ref(
  route.query.registered === 'true'
    ? 'Your account has been created. You can now sign in.'
    : '',
)

async function handleLogin() {
  error.value = ''
  success.value = ''

  if (!email.value.trim() || !password.value) {
    error.value = 'Please enter your email and password.'
    return
  }

  loading.value = true

  try {
    const response = await api.post<LoginResponse>('/auth/login/', {
      email: email.value.trim().toLowerCase(),
      password: password.value,
    })

    const data = response.data
    const user = {
      username: data.username,
      email: data.email,
      role: data.role || (data.is_admin ? 'admin' : 'user'),
      is_admin: data.is_admin ?? data.role?.toLowerCase() === 'admin',
    }

    localStorage.setItem('fids_access_token', data.access)
    localStorage.setItem('fids_refresh_token', data.refresh)
    localStorage.setItem('fids_user', JSON.stringify(user))

    // Remove legacy credentials if present.
    localStorage.removeItem('token')
    localStorage.removeItem('user')
    sessionStorage.removeItem('token')
    sessionStorage.removeItem('user')

    const requestedRedirect = typeof route.query.redirect === 'string'
      ? route.query.redirect
      : ''

    // Only allow internal application paths as redirects.
    if (requestedRedirect.startsWith('/') && !requestedRedirect.startsWith('//')) {
      await router.replace(requestedRedirect)
    } else if (user.is_admin) {
      await router.replace('/admin/dashboard')
    } else {
      await router.replace('/account/profile')
    }
  } catch (err: any) {
    const data = err.response?.data

    error.value =
      data?.detail ||
      data?.message ||
      'Invalid email or password. Please try again.'
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
          <h1 class="text-2xl font-bold">Welcome back</h1>
          <p class="mt-2 text-sm text-slate-400">
            Sign in to your FIDS account.
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

        <form class="space-y-5" @submit.prevent="handleLogin">
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
            <div class="mb-2 flex items-center justify-between gap-3">
              <label for="password" class="text-sm font-medium">Password</label>
              <RouterLink
                to="/auth/forgot-password"
                class="text-sm text-blue-400 hover:text-blue-300"
              >
                Forgot password?
              </RouterLink>
            </div>
            <div class="relative">
              <LockKeyhole class="absolute left-3 top-1/2 h-5 w-5 -translate-y-1/2 text-slate-500" />
              <input
                id="password"
                v-model="password"
                type="password"
                autocomplete="current-password"
                required
                placeholder="Enter your password"
                class="w-full rounded-xl border border-[#293342] bg-[#090D13] py-3 pl-11 pr-4 outline-none transition focus:border-blue-500"
              />
            </div>
          </div>

          <button
            type="submit"
            :disabled="loading"
            class="flex w-full items-center justify-center gap-2 rounded-xl bg-blue-600 px-4 py-3 font-semibold transition hover:bg-blue-500 disabled:cursor-not-allowed disabled:opacity-60"
          >
            {{ loading ? 'Signing in...' : 'Sign in' }}
            <ArrowRight v-if="!loading" class="h-4 w-4" />
          </button>
        </form>

        <p class="mt-6 text-center text-sm text-slate-400">
          Don't have an account?
          <RouterLink to="/auth/register" class="font-semibold text-blue-400 hover:text-blue-300">
            Create account
          </RouterLink>
        </p>
      </div>
    </div>
  </main>
</template>