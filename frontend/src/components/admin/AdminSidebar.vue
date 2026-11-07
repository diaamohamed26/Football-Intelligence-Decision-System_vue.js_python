<template>
  <aside
    class="fixed inset-y-0 left-0 z-50 flex w-64 flex-col
           border-r border-white/[0.06] bg-slate-950 text-white"
  >
    <!-- Brand -->
    <div
      class="flex h-[76px] shrink-0 items-center gap-3
             border-b border-white/[0.07] px-5"
    >
      <div
        class="flex h-11 w-11 items-center justify-center rounded-2xl
               bg-gradient-to-br from-blue-500 to-indigo-700
               text-xl font-black shadow-lg shadow-blue-950/50"
      >
        F
      </div>

      <div class="min-w-0 flex-1">
        <h1 class="text-lg font-extrabold tracking-wide">FIDS</h1>
        <p class="mt-0.5 text-[10px] font-medium tracking-wider text-slate-500">
          FOOTBALL INTELLIGENCE
        </p>
      </div>

      <span
        class="rounded-md border border-blue-400/20 bg-blue-500/10
               px-1.5 py-1 text-[9px] font-bold uppercase
               tracking-wider text-blue-300"
      >
        Admin
      </span>
    </div>

    <!-- User status -->
    <div class="mx-4 mt-5 rounded-xl border border-white/[0.06]
                bg-white/[0.025] p-3">
      <div class="flex items-center gap-3">
        <div
          class="relative flex h-10 w-10 shrink-0 items-center
                 justify-center rounded-xl bg-gradient-to-br
                 from-blue-500 to-indigo-600 text-sm font-bold"
        >
          {{ initials }}

          <span
            class="absolute -bottom-1 -right-1 h-3 w-3 rounded-full
                   border-2 border-slate-950 bg-emerald-400"
          />
        </div>

        <div class="min-w-0 flex-1">
          <p class="truncate text-sm font-semibold">{{ displayName }}</p>
          <p class="mt-1 truncate text-xs text-slate-500">{{ roleLabel }}</p>
        </div>

        <span
          class="h-2 w-2 shrink-0 rounded-full bg-emerald-400"
          title="Signed in"
        />
      </div>
    </div>

    <!-- Navigation -->
    <nav class="flex-1 space-y-6 overflow-y-auto px-3 py-6">
      <section v-for="group in navigation" :key="group.title">
        <p
          class="mb-2 px-3 text-[10px] font-bold uppercase
                 tracking-[0.18em] text-slate-600"
        >
          {{ group.title }}
        </p>

        <div class="space-y-1">
          <RouterLink
            v-for="item in group.items"
            :key="item.to"
            :to="item.to"
            class="group relative flex h-11 items-center gap-3
                   rounded-xl px-3 text-[13px] font-medium transition"
            :class="isItemActive(item.to)
              ? 'bg-blue-600/15 text-blue-300'
              : 'text-slate-400 hover:bg-white/[0.045] hover:text-white'"
          >
            <span
              v-if="isItemActive(item.to)"
              class="absolute bottom-2 left-0 top-2 w-[3px]
                     rounded-r-full bg-blue-400"
            />

            <component
              :is="item.icon"
              class="h-[18px] w-[18px] shrink-0"
              :class="isItemActive(item.to)
                ? 'text-blue-400'
                : 'text-slate-500 group-hover:text-slate-200'"
              :stroke-width="1.8"
            />

            <span class="flex-1">{{ item.label }}</span>

            <ChevronRight
              v-if="isItemActive(item.to)"
              class="h-4 w-4 text-blue-400"
            />
          </RouterLink>
        </div>
      </section>

      <!-- Account -->
      <section>
        <p
          class="mb-2 px-3 text-[10px] font-bold uppercase
                 tracking-[0.18em] text-slate-600"
        >
          Account
        </p>

        <RouterLink
          to="/admin/profile"
          class="group flex h-11 items-center gap-3 rounded-xl
                 px-3 text-[13px] font-medium transition"
          :class="isProfileActive
            ? 'bg-blue-600/15 text-blue-300'
            : 'text-slate-400 hover:bg-white/[0.045] hover:text-white'"
        >
          <UserCircle
            class="h-[18px] w-[18px]"
            :class="isProfileActive
              ? 'text-blue-400'
              : 'text-slate-500 group-hover:text-slate-200'"
          />

          <span class="flex-1">My Profile</span>

          <ChevronRight
            v-if="isProfileActive"
            class="h-4 w-4 text-blue-400"
          />
        </RouterLink>

        <RouterLink
          to="/"
          class="mt-1 flex h-11 items-center gap-3 rounded-xl
                 px-3 text-[13px] font-medium text-slate-400
                 transition hover:bg-white/[0.045] hover:text-white"
        >
          <ExternalLink class="h-[18px] w-[18px] text-slate-500" />
          <span class="flex-1">View Website</span>
        </RouterLink>
      </section>
    </nav>

    <!-- Footer -->
    <div class="shrink-0 border-t border-white/[0.07] p-3">
      <div class="mb-3 flex items-center gap-3 rounded-xl px-2 py-2">
        <div
          class="flex h-9 w-9 items-center justify-center
                 rounded-full bg-slate-800 text-slate-300"
        >
          <CircleUserRound class="h-5 w-5" />
        </div>

        <div class="min-w-0 flex-1">
          <p class="truncate text-xs font-semibold text-slate-200">
            FIDS Control Center
          </p>
          <p class="mt-1 text-[10px] text-slate-500">
            Management workspace
          </p>
        </div>
      </div>

      <button
        type="button"
        class="flex h-10 w-full items-center gap-3 rounded-xl
               px-3 text-xs font-medium text-slate-400
               transition hover:bg-rose-500/10 hover:text-rose-300"
        @click="logout"
      >
        <LogOut class="h-[17px] w-[17px]" />
        Sign out
      </button>

      <p class="px-3 pb-1 pt-3 text-center text-[10px] text-slate-700">
        FIDS Admin · v1.0.0
      </p>
    </div>
  </aside>
</template>

<script setup lang="ts">
import { computed, ref, watch } from 'vue'
import { RouterLink, useRoute, useRouter } from 'vue-router'
import {
  LayoutDashboard,
  Users,
  Swords,
  Shield,
  UserRound,
  Trophy,
  Newspaper,
  ScanSearch,
  BrainCircuit,
  Settings,
  ExternalLink,
  UserCircle,
  ChevronRight,
  LogOut,
  CircleUserRound,
} from 'lucide-vue-next'

interface FidsUser {
  username?: string
  name?: string
  first_name?: string
  last_name?: string
  role?: string
  is_staff?: boolean
  is_superuser?: boolean
}

const route = useRoute()
const router = useRouter()

const navigation = [
  {
    title: 'Main',
    items: [
      { label: 'Dashboard', to: '/admin/dashboard', icon: LayoutDashboard },
    ],
  },
  {
    title: 'Management',
    items: [
      { label: 'Users', to: '/admin/users', icon: Users },
      { label: 'Matches', to: '/admin/matches', icon: Swords },
      { label: 'Teams', to: '/admin/teams', icon: Shield },
      { label: 'Players', to: '/admin/players', icon: UserRound },
      { label: 'Competitions', to: '/admin/competitions', icon: Trophy },
      { label: 'News', to: '/admin/news', icon: Newspaper },
    ],
  },
  {
    title: 'Intelligence',
    items: [
      { label: 'Scouting', to: '/admin/scouting', icon: ScanSearch },
      { label: 'Intelligence', to: '/admin/intelligence', icon: BrainCircuit },
    ],
  },
  {
    title: 'System',
    items: [
      { label: 'Settings', to: '/admin/settings', icon: Settings },
    ],
  },
]

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

  return user.value?.name || fullName || user.value?.username || 'Administrator'
})

const initials = computed(() =>
  displayName.value
    .split(/\s+/)
    .filter(Boolean)
    .slice(0, 2)
    .map((part) => part[0].toUpperCase())
    .join('') || 'A',
)

const roleLabel = computed(() => {
  if (user.value?.is_superuser) return 'Super Admin'
  if (user.value?.is_staff) return 'Admin'
  return user.value?.role || 'Account'
})

const isProfileActive = computed(() => route.path === '/admin/profile')

function isItemActive(path: string): boolean {
  if (path === '/admin/dashboard') {
    return route.path === path
  }

  return route.path === path || route.path.startsWith(`${path}/`)
}

async function logout() {
  const authKeys = [
    'fids_access_token',
    'fids_refresh_token',
    'fids_user',
    'access',
    'access_token',
    'accessToken',
    'token',
    'user',
  ]

  for (const storage of [localStorage, sessionStorage]) {
    authKeys.forEach((key) => storage.removeItem(key))
  }

  user.value = null

  await router.replace({ name: 'login' })
}

watch(
  () => route.fullPath,
  () => {
    user.value = readUser()
  },
)
</script>
