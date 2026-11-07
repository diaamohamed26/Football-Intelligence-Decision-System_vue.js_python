<script setup lang="ts">
import { computed, ref, watch } from 'vue'
import { RouterLink, useRoute, useRouter } from 'vue-router'
import {
  Search,
  Menu,
  X,
  Zap,
  UserRound,
  LayoutDashboard,
  LogOut,
} from 'lucide-vue-next'

const route = useRoute()
const router = useRouter()

const mobileOpen = ref(false)

interface StoredUser {
  username?: string
  email?: string
  role?: string
  is_admin?: boolean
  isAdmin?: boolean
}

const navItems = [
  { name: 'Home', path: '/' },
  { name: 'Live', path: '/live' },
  { name: 'Matches', path: '/matches' },
  { name: 'Teams', path: '/teams' },
  { name: 'Players', path: '/players' },
  { name: 'Intelligence', path: '/intelligence' },
  { name: 'Scouting', path: '/scouting' },
  { name: 'News', path: '/news' },
]

const activeClass = '!bg-[#151C26] !text-[#B7FF3C]'

const currentUser = ref<StoredUser | null>(null)
const isAuthenticated = ref(false)

const isAdmin = computed(() => {
  return (
    currentUser.value?.role?.toLowerCase() === 'admin' ||
    currentUser.value?.is_admin === true ||
    currentUser.value?.isAdmin === true
  )
})

const accountPath = computed(() =>
  isAdmin.value ? '/admin/dashboard' : '/account/profile',
)

const accountLabel = computed(() =>
  isAdmin.value ? 'Admin Dashboard' : 'My Profile',
)

function syncAuthState() {
  currentUser.value = null
  isAuthenticated.value = false

  for (const storage of [localStorage, sessionStorage]) {
    const token =
      storage.getItem('fids_access_token') || storage.getItem('token')

    if (!token) continue

    isAuthenticated.value = true

    const userRaw =
      storage.getItem('fids_user') || storage.getItem('user')

    try {
      currentUser.value = userRaw ? JSON.parse(userRaw) : null
    } catch {
      currentUser.value = null
    }

    return
  }
}

function closeMobileMenu() {
  mobileOpen.value = false
}

function toggleMobileMenu() {
  mobileOpen.value = !mobileOpen.value
}

async function logout() {
  const authKeys = [
    'fids_access_token',
    'fids_refresh_token',
    'fids_user',
    'token',
    'user',
  ]

  for (const storage of [localStorage, sessionStorage]) {
    authKeys.forEach((key) => storage.removeItem(key))
  }

  syncAuthState()
  closeMobileMenu()

  await router.replace({ name: 'login' })
}

watch(
  () => route.fullPath,
  () => {
    closeMobileMenu()
    syncAuthState()
  },
  { immediate: true },
)
</script>

<template>
  <header
    class="sticky top-0 z-50 border-b border-white/5 bg-[#080B10]/95 backdrop-blur-xl"
  >
    <div
      class="mx-auto flex h-16 max-w-[1600px] items-center justify-between px-4 sm:px-6 lg:px-8"
    >
      <!-- Logo -->
      <RouterLink
        to="/"
        class="flex items-center gap-2.5"
        aria-label="FIDS Home"
      >
        <div
          class="flex h-9 w-9 items-center justify-center rounded-xl bg-[#B7FF3C] text-[#080B10]"
        >
          <Zap :size="19" :stroke-width="2.5" />
        </div>

        <div class="hidden sm:block">
          <div class="text-base font-bold tracking-wide text-white">FIDS</div>
          <div
            class="text-[9px] font-medium uppercase tracking-[0.2em] text-[#697386]"
          >
            Football Intelligence
          </div>
        </div>
      </RouterLink>

      <!-- Desktop Navigation -->
      <nav
        class="hidden items-center gap-1 lg:flex"
        aria-label="Main navigation"
      >
        <RouterLink
          v-for="item in navItems"
          :key="item.path"
          :to="item.path"
          :exact-active-class="activeClass"
          class="rounded-lg px-3 py-2 text-sm font-medium text-[#8993A4] transition-all duration-200 hover:bg-[#0F141C] hover:text-white"
        >
          {{ item.name }}
        </RouterLink>
      </nav>

      <!-- Desktop Actions -->
      <div class="hidden items-center gap-2 lg:flex">
        <RouterLink
          to="/search"
          class="flex h-9 w-9 items-center justify-center rounded-lg text-[#8993A4] transition hover:bg-[#0F141C] hover:text-white"
          aria-label="Search"
        >
          <Search :size="18" />
        </RouterLink>

        <RouterLink
          to="/ai"
          class="flex items-center gap-2 rounded-lg border border-[#B7FF3C]/20 bg-[#B7FF3C]/5 px-3 py-2 text-sm font-semibold text-[#B7FF3C] transition hover:border-[#B7FF3C]/40 hover:bg-[#B7FF3C]/10"
        >
          <Zap :size="15" />
          FIDS AI
        </RouterLink>

        <template v-if="isAuthenticated">
          <RouterLink
            :to="accountPath"
            class="flex items-center gap-2 rounded-lg bg-[#151C26] px-3 py-2 text-sm font-medium text-white transition hover:bg-[#1C2531]"
          >
            <LayoutDashboard v-if="isAdmin" :size="16" />
            <UserRound v-else :size="16" />
            {{ accountLabel }}
          </RouterLink>

          <button
            type="button"
            class="flex h-9 items-center gap-2 rounded-lg px-3 text-sm font-medium text-[#8993A4] transition hover:bg-rose-500/10 hover:text-rose-300"
            @click="logout"
          >
            <LogOut :size="16" />
            Sign out
          </button>
        </template>

        <RouterLink
          v-else
          to="/auth/login"
          class="flex items-center gap-2 rounded-lg bg-[#151C26] px-3 py-2 text-sm font-medium text-white transition hover:bg-[#1C2531]"
        >
          <UserRound :size="16" />
          Login
        </RouterLink>
      </div>

      <!-- Mobile Menu Button -->
      <button
        type="button"
        class="flex h-9 w-9 items-center justify-center rounded-lg text-[#8993A4] transition hover:bg-[#0F141C] hover:text-white lg:hidden"
        :aria-label="mobileOpen ? 'Close menu' : 'Open menu'"
        :aria-expanded="mobileOpen"
        @click="toggleMobileMenu"
      >
        <X v-if="mobileOpen" :size="21" />
        <Menu v-else :size="21" />
      </button>
    </div>

    <!-- Mobile Navigation -->
    <Transition
      enter-active-class="transition duration-200 ease-out"
      enter-from-class="opacity-0 -translate-y-2"
      enter-to-class="opacity-100 translate-y-0"
      leave-active-class="transition duration-150 ease-in"
      leave-from-class="opacity-100 translate-y-0"
      leave-to-class="opacity-0 -translate-y-2"
    >
      <div
        v-if="mobileOpen"
        class="border-t border-white/5 bg-[#080B10] lg:hidden"
      >
        <nav
          class="mx-auto max-w-[1600px] space-y-1 px-4 py-4 sm:px-6"
          aria-label="Mobile navigation"
        >
          <RouterLink
            v-for="item in navItems"
            :key="item.path"
            :to="item.path"
            :exact-active-class="activeClass"
            class="block rounded-lg px-4 py-3 text-sm font-medium text-[#8993A4] transition-all duration-200 hover:bg-[#0F141C] hover:text-white"
            @click="closeMobileMenu"
          >
            {{ item.name }}
          </RouterLink>

          <div class="mt-3 border-t border-white/5 pt-3">
            <RouterLink
              to="/search"
              class="flex items-center gap-3 rounded-lg px-4 py-3 text-sm font-medium text-[#8993A4] transition hover:bg-[#0F141C] hover:text-white"
              @click="closeMobileMenu"
            >
              <Search :size="17" />
              Search
            </RouterLink>

            <RouterLink
              to="/ai"
              class="mt-1 flex items-center gap-3 rounded-lg px-4 py-3 text-sm font-semibold text-[#B7FF3C] transition hover:bg-[#B7FF3C]/10"
              @click="closeMobileMenu"
            >
              <Zap :size="17" />
              FIDS AI
            </RouterLink>

            <template v-if="isAuthenticated">
              <RouterLink
                :to="accountPath"
                class="mt-1 flex items-center gap-3 rounded-lg px-4 py-3 text-sm font-medium text-white transition hover:bg-[#151C26]"
                @click="closeMobileMenu"
              >
                <LayoutDashboard v-if="isAdmin" :size="17" />
                <UserRound v-else :size="17" />
                {{ accountLabel }}
              </RouterLink>

              <button
                type="button"
                class="mt-1 flex w-full items-center gap-3 rounded-lg px-4 py-3 text-sm font-medium text-[#8993A4] transition hover:bg-rose-500/10 hover:text-rose-300"
                @click="logout"
              >
                <LogOut :size="17" />
                Sign out
              </button>
            </template>

            <RouterLink
              v-else
              to="/auth/login"
              class="mt-1 flex items-center gap-3 rounded-lg px-4 py-3 text-sm font-medium text-white transition hover:bg-[#151C26]"
              @click="closeMobileMenu"
            >
              <UserRound :size="17" />
              Login
            </RouterLink>
          </div>
        </nav>
      </div>
    </Transition>
  </header>
</template>
