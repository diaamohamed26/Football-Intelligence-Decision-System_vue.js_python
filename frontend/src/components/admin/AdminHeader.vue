<template>
  <header
    class="sticky top-0 z-40 flex h-20 items-center justify-between
           border-b border-white/[0.07] bg-slate-950/95 px-4 text-white
           backdrop-blur-xl sm:px-6 lg:px-8"
  >
    <div class="min-w-0">
      <h2 class="truncate text-lg font-bold">
        {{ pageTitle }}
      </h2>

      <p class="mt-1 text-xs text-slate-500">
        Football Intelligence Decision System
      </p>
    </div>

    <div class="flex items-center gap-3 sm:gap-5">
      <!-- Notifications -->
      <div class="relative">
        <button
          type="button"
          aria-label="Notifications"
          :aria-expanded="showNotifications"
          class="relative flex h-10 w-10 items-center justify-center
                 rounded-xl border border-white/[0.07] bg-white/[0.03]
                 text-slate-300 transition hover:bg-white/[0.08]
                 hover:text-white"
          @click="showNotifications = !showNotifications"
        >
          <Bell class="h-5 w-5" />

          <span
            v-if="notifications.length"
            class="absolute right-2 top-2 h-2 w-2 rounded-full
                   bg-rose-500 ring-2 ring-slate-950"
          />
        </button>

        <div
          v-if="showNotifications"
          class="absolute right-0 top-12 z-50 w-72 rounded-xl
                 border border-white/10 bg-slate-900 p-4 shadow-2xl"
        >
          <div class="flex items-center justify-between">
            <h3 class="text-sm font-semibold">Notifications</h3>

            <button
              type="button"
              class="text-xs text-slate-400 hover:text-white"
              @click="showNotifications = false"
            >
              Close
            </button>
          </div>

          <p class="mt-4 text-sm text-slate-400">
            {{ notifications.length
              ? 'You have notifications to review.'
              : 'You are all caught up.' }}
          </p>
        </div>
      </div>

      <!-- User profile -->
      <RouterLink
        to="/admin/profile"
        class="flex items-center gap-3 rounded-xl p-1.5 transition
               hover:bg-white/[0.05]"
        aria-label="Open admin profile"
      >
        <div
          class="flex h-10 w-10 shrink-0 items-center justify-center
                 rounded-xl bg-gradient-to-br from-blue-500 to-indigo-600
                 text-sm font-bold text-white"
        >
          {{ initials }}
        </div>

        <div class="hidden min-w-0 sm:block">
          <p class="max-w-40 truncate text-sm font-semibold text-white">
            {{ displayName }}
          </p>

          <p class="mt-1 text-xs text-slate-500">
            {{ roleLabel }}
          </p>
        </div>

        <ChevronDown class="hidden h-4 w-4 text-slate-500 sm:block" />
      </RouterLink>
    </div>
  </header>
</template>

<script setup lang="ts">
import { computed, ref, watch } from 'vue'
import { RouterLink, useRoute } from 'vue-router'
import { Bell, ChevronDown } from 'lucide-vue-next'

interface FidsUser {
  id?: number
  username?: string
  name?: string
  first_name?: string
  last_name?: string
  email?: string
  role?: string
  is_staff?: boolean
  is_superuser?: boolean
}

const route = useRoute()
const showNotifications = ref(false)
const notifications = ref<string[]>([])

function readUser(): FidsUser | null {
  try {
    const raw =
      localStorage.getItem('fids_user') ||
      sessionStorage.getItem('fids_user')

    return raw ? (JSON.parse(raw) as FidsUser) : null
  } catch {
    return null
  }
}

const user = ref<FidsUser | null>(readUser())

const displayName = computed(() => {
  const fullName = [user.value?.first_name, user.value?.last_name]
    .filter(Boolean)
    .join(' ')
    .trim()

  return (
    user.value?.name ||
    fullName ||
    user.value?.username ||
    'Administrator'
  )
})

const initials = computed(() => {
  const name = displayName.value.trim()

  if (!name) return 'A'

  return name
    .split(/\s+/)
    .slice(0, 2)
    .map((part) => part.charAt(0).toUpperCase())
    .join('')
})

const roleLabel = computed(() => {
  if (user.value?.is_superuser) return 'Super Admin'
  if (user.value?.is_staff) return 'Admin'
  return user.value?.role || 'Account'
})

const pageTitle = computed(() => {
  const titles: Record<string, string> = {
    '/admin/dashboard': 'Admin Dashboard',
    '/admin/users': 'User Management',
    '/admin/matches': 'Match Management',
    '/admin/teams': 'Team Management',
    '/admin/players': 'Player Management',
    '/admin/competitions': 'Competition Management',
    '/admin/news': 'News Management',
    '/admin/scouting': 'Scouting Center',
    '/admin/intelligence': 'Football Intelligence',
    '/admin/settings': 'System Settings',
    '/admin/profile': 'My Profile',
  }

  return titles[route.path] || 'FIDS Admin'
})

watch(
  () => route.fullPath,
  () => {
    showNotifications.value = false
    user.value = readUser()
  },
)
</script>
