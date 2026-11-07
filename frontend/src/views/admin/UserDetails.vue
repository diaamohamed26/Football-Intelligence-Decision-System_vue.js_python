<script setup lang="ts">
import { computed, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'

type UserRole = 'Admin' | 'Analyst' | 'Scout' | 'User'
type UserStatus = 'Active' | 'Inactive' | 'Suspended'

interface Activity {
  id: number
  action: string
  description: string
  date: string
  type: 'login' | 'update' | 'report' | 'security'
}

interface UserRecord {
  id: number
  name: string
  email: string
  phone: string
  role: UserRole
  status: UserStatus
  country: string
  joinedAt: string
  lastLogin: string
  department: string
  bio: string
  emailVerified: boolean
  twoFactorEnabled: boolean
  favoriteLeague: string
  activities: Activity[]
}

const route = useRoute()
const router = useRouter()

// Demo data only. Replace with the user returned by your Django API.
const users = ref<UserRecord[]>([
  {
    id: 1,
    name: 'Ahmed Hassan',
    email: 'ahmed.hassan@example.com',
    phone: '+20 100 123 4567',
    role: 'Admin',
    status: 'Active',
    country: 'Egypt',
    joinedAt: '2025-01-12',
    lastLogin: '2026-10-10 14:25',
    department: 'Administration',
    bio: 'Platform administrator responsible for user management and system operations.',
    emailVerified: true,
    twoFactorEnabled: true,
    favoriteLeague: 'Premier League',
    activities: [
      { id: 1, action: 'Logged in', description: 'Signed in to the admin dashboard.', date: '2026-10-10 14:25', type: 'login' },
      { id: 2, action: 'Updated settings', description: 'Changed platform configuration preferences.', date: '2026-10-10 13:40', type: 'update' },
      { id: 3, action: 'Generated report', description: 'Created a football intelligence report.', date: '2026-10-09 16:15', type: 'report' },
      { id: 4, action: 'Security check', description: 'Account security verification completed.', date: '2026-10-08 11:20', type: 'security' },
    ],
  },
  {
    id: 2,
    name: 'Sara Mohamed',
    email: 'sara.mohamed@example.com',
    phone: '+20 111 234 5678',
    role: 'Analyst',
    status: 'Active',
    country: 'Egypt',
    joinedAt: '2025-03-05',
    lastLogin: '2026-10-09 10:15',
    department: 'Football Analytics',
    bio: 'Football analyst working with match statistics and performance insights.',
    emailVerified: true,
    twoFactorEnabled: false,
    favoriteLeague: 'La Liga',
    activities: [
      { id: 1, action: 'Logged in', description: 'Signed in to the platform.', date: '2026-10-09 10:15', type: 'login' },
      { id: 2, action: 'Generated report', description: 'Reviewed a match analysis report.', date: '2026-10-08 15:30', type: 'report' },
    ],
  },
  {
    id: 3,
    name: 'Omar Ali',
    email: 'omar.ali@example.com',
    phone: '+20 122 345 6789',
    role: 'Scout',
    status: 'Inactive',
    country: 'Egypt',
    joinedAt: '2025-06-20',
    lastLogin: '2026-09-18 09:05',
    department: 'Scouting',
    bio: 'Football scout tracking player prospects and emerging talent.',
    emailVerified: false,
    twoFactorEnabled: false,
    favoriteLeague: 'Egyptian Premier League',
    activities: [
      { id: 1, action: 'Updated profile', description: 'Updated scouting profile details.', date: '2026-09-18 09:05', type: 'update' },
    ],
  },
])

const userId = computed(() => Number(route.params.id) || 1)
const user = computed(() => users.value.find((item) => item.id === userId.value) ?? null)

const showEditModal = ref(false)
const showStatusConfirm = ref(false)
const showDeleteConfirm = ref(false)
const toast = ref('')
const formError = ref('')

const editForm = ref({
  name: '',
  email: '',
  phone: '',
  role: 'User' as UserRole,
  country: '',
  department: '',
  bio: '',
  favoriteLeague: '',
})

const initials = computed(() => {
  if (!user.value) return 'U'
  return user.value.name
    .trim()
    .split(/\s+/)
    .slice(0, 2)
    .map((part) => part.charAt(0))
    .join('')
    .toUpperCase()
})

const accountAge = computed(() => {
  if (!user.value) return '—'

  const joined = new Date(user.value.joinedAt)
  if (Number.isNaN(joined.getTime())) return '—'

  const days = Math.max(
    0,
    Math.floor((Date.now() - joined.getTime()) / (1000 * 60 * 60 * 24)),
  )

  if (days < 30) return `${days} days`
  if (days < 365) return `${Math.floor(days / 30)} months`
  return `${Math.floor(days / 365)} years`
})

const roleDescription = computed(() => {
  const descriptions: Record<UserRole, string> = {
    Admin: 'Can manage platform operations and user access.',
    Analyst: 'Works with match data, statistics, and intelligence reports.',
    Scout: 'Tracks player prospects and scouting recommendations.',
    User: 'Has standard access to permitted platform features.',
  }

  return user.value ? descriptions[user.value.role] : ''
})

function openEdit() {
  if (!user.value) return

  editForm.value = {
    name: user.value.name,
    email: user.value.email,
    phone: user.value.phone,
    role: user.value.role,
    country: user.value.country,
    department: user.value.department,
    bio: user.value.bio,
    favoriteLeague: user.value.favoriteLeague,
  }

  formError.value = ''
  showEditModal.value = true
}

function saveEdit() {
  if (!user.value) return

  const name = editForm.value.name.trim()
  const email = editForm.value.email.trim()

  if (!name || !email) {
    formError.value = 'Name and email are required.'
    return
  }

  const duplicate = users.value.some(
    (item) =>
      item.id !== user.value!.id &&
      item.email.toLowerCase() === email.toLowerCase(),
  )

  if (duplicate) {
    formError.value = 'Another user already uses this email address.'
    return
  }

  Object.assign(user.value, {
    ...editForm.value,
    name,
    email,
  })

  user.value.activities.unshift({
    id: Date.now(),
    action: 'Profile updated',
    description: 'User information was updated from the admin dashboard.',
    date: new Date().toLocaleString(),
    type: 'update',
  })

  showEditModal.value = false
  notify('User profile updated in the demo session.')
}

function toggleStatus() {
  if (!user.value) return

  user.value.status = user.value.status === 'Active' ? 'Suspended' : 'Active'

  user.value.activities.unshift({
    id: Date.now(),
    action: user.value.status === 'Active' ? 'Account activated' : 'Account suspended',
    description: 'Account status changed from the admin dashboard.',
    date: new Date().toLocaleString(),
    type: 'security',
  })

  showStatusConfirm.value = false
  notify(`Account marked as ${user.value.status.toLowerCase()} in the demo session.`)
}

function deleteUser() {
  if (!user.value) return

  const id = user.value.id
  users.value = users.value.filter((item) => item.id !== id)
  showDeleteConfirm.value = false

  notify('Demo user removed.')
  router.push('/admin/users')
}

function notify(message: string) {
  toast.value = message
}

function activityIcon(type: Activity['type']) {
  const icons: Record<Activity['type'], string> = {
    login: '↗',
    update: '✎',
    report: '▤',
    security: '⬡',
  }

  return icons[type]
}

function activityColor(type: Activity['type']) {
  const colors: Record<Activity['type'], string> = {
    login: 'bg-cyan-400/10 text-cyan-300',
    update: 'bg-violet-400/10 text-violet-300',
    report: 'bg-emerald-400/10 text-emerald-300',
    security: 'bg-amber-400/10 text-amber-300',
  }

  return colors[type]
}
</script>

<template>
  <div class="min-h-screen bg-[#090d16] px-4 py-6 text-slate-100 sm:px-6 lg:px-8">
    <div class="mx-auto max-w-7xl space-y-7">
      <!-- Header -->
      <header class="flex flex-col justify-between gap-4 sm:flex-row sm:items-center">
        <div>
          <button
            type="button"
            class="mb-4 inline-flex items-center gap-2 text-sm text-slate-400 transition hover:text-cyan-300"
            @click="router.push('/admin/users')"
          >
            <span>←</span> Back to users
          </button>

          <div class="text-xs font-semibold uppercase tracking-[0.22em] text-cyan-400">
            User management
          </div>

          <h1 class="mt-2 text-3xl font-bold tracking-tight text-white sm:text-4xl">
            User details<span class="text-cyan-400">.</span>
          </h1>

          <p class="mt-2 text-sm text-slate-400">
            View account information, permissions, and recent activity.
          </p>
        </div>

        <div v-if="user" class="flex flex-wrap gap-3">
          <button
            type="button"
            class="rounded-xl border border-slate-700 px-4 py-2.5 text-sm font-semibold text-slate-300 transition hover:bg-slate-800 hover:text-white"
            @click="showStatusConfirm = true"
          >
            {{ user.status === 'Active' ? 'Suspend account' : 'Activate account' }}
          </button>

          <button
            type="button"
            class="rounded-xl bg-cyan-400 px-5 py-2.5 text-sm font-bold text-slate-950 transition hover:bg-cyan-300"
            @click="openEdit"
          >
            ✎ Edit user
          </button>
        </div>
      </header>

      <!-- Toast -->
      <div
        v-if="toast"
        class="flex items-center justify-between gap-3 rounded-xl border border-emerald-500/30 bg-emerald-500/10 px-4 py-3 text-sm text-emerald-300"
        role="status"
      >
        <span>{{ toast }}</span>
        <button type="button" aria-label="Dismiss message" @click="toast = ''">✕</button>
      </div>

      <!-- Missing user -->
      <section v-if="!user" class="rounded-2xl border border-slate-800 bg-[#0e1420] px-6 py-16 text-center">
        <div class="mx-auto flex h-14 w-14 items-center justify-center rounded-2xl bg-slate-800 text-2xl">?</div>
        <h2 class="mt-4 text-xl font-bold text-white">User not found</h2>
        <p class="mt-2 text-sm text-slate-400">
          No demo user matches ID {{ route.params.id }}.
        </p>
        <button
          type="button"
          class="mt-5 rounded-xl bg-cyan-400 px-5 py-3 text-sm font-bold text-slate-950"
          @click="router.push('/admin/users')"
        >
          Return to users
        </button>
      </section>

      <template v-else>
        <!-- Profile banner -->
        <section class="overflow-hidden rounded-2xl border border-slate-800 bg-[#0e1420]">
          <div class="h-28 bg-gradient-to-r from-cyan-500/20 via-blue-500/10 to-violet-500/20"></div>

          <div class="px-5 pb-6 sm:px-7">
            <div class="-mt-11 flex flex-col justify-between gap-5 sm:flex-row sm:items-end">
              <div class="flex flex-col gap-4 sm:flex-row sm:items-end">
                <div class="flex h-24 w-24 items-center justify-center rounded-2xl border-4 border-[#0e1420] bg-gradient-to-br from-cyan-400 to-blue-600 text-2xl font-black text-slate-950 shadow-xl">
                  {{ initials }}
                </div>

                <div class="pb-1">
                  <h2 class="text-2xl font-bold text-white">{{ user.name }}</h2>
                  <p class="mt-1 text-sm text-slate-400">{{ user.email }}</p>

                  <div class="mt-3 flex flex-wrap items-center gap-2">
                    <span class="rounded-lg border border-cyan-400/20 bg-cyan-400/10 px-2.5 py-1 text-xs font-semibold text-cyan-300">
                      {{ user.role }}
                    </span>

                    <span
                      class="inline-flex items-center gap-2 rounded-lg px-2.5 py-1 text-xs font-semibold"
                      :class="user.status === 'Active'
                        ? 'bg-emerald-400/10 text-emerald-300'
                        : user.status === 'Suspended'
                          ? 'bg-rose-400/10 text-rose-300'
                          : 'bg-slate-700/60 text-slate-400'"
                    >
                      <span
                        class="h-1.5 w-1.5 rounded-full"
                        :class="user.status === 'Active'
                          ? 'bg-emerald-400'
                          : user.status === 'Suspended'
                            ? 'bg-rose-400'
                            : 'bg-slate-500'"
                      ></span>
                      {{ user.status }}
                    </span>

                    <span
                      v-if="user.emailVerified"
                      class="rounded-lg bg-emerald-400/10 px-2.5 py-1 text-xs font-semibold text-emerald-300"
                    >
                      ✓ Email verified
                    </span>
                  </div>
                </div>
              </div>

              <div class="rounded-xl border border-slate-800 bg-[#090d16] px-4 py-3 sm:min-w-36">
                <p class="text-xs text-slate-500">Member since</p>
                <p class="mt-1 font-semibold text-white">{{ user.joinedAt }}</p>
                <p class="mt-1 text-xs text-slate-500">{{ accountAge }}</p>
              </div>
            </div>
          </div>
        </section>

        <!-- Stats -->
        <section class="grid grid-cols-1 gap-4 sm:grid-cols-2 xl:grid-cols-4">
          <article class="rounded-2xl border border-slate-800 bg-[#0e1420] p-5">
            <div class="flex items-center justify-between">
              <span class="text-sm text-slate-400">Account status</span>
              <span class="text-lg text-emerald-300">●</span>
            </div>
            <p class="mt-4 text-2xl font-bold text-white">{{ user.status }}</p>
            <p class="mt-2 text-xs text-slate-500">Current account state</p>
          </article>

          <article class="rounded-2xl border border-slate-800 bg-[#0e1420] p-5">
            <div class="flex items-center justify-between">
              <span class="text-sm text-slate-400">Recent activities</span>
              <span class="text-lg text-cyan-300">↗</span>
            </div>
            <p class="mt-4 text-2xl font-bold text-white">{{ user.activities.length }}</p>
            <p class="mt-2 text-xs text-slate-500">Sample activity records</p>
          </article>

          <article class="rounded-2xl border border-slate-800 bg-[#0e1420] p-5">
            <div class="flex items-center justify-between">
              <span class="text-sm text-slate-400">Email verification</span>
              <span class="text-lg" :class="user.emailVerified ? 'text-emerald-300' : 'text-amber-300'">
                {{ user.emailVerified ? '✓' : '!' }}
              </span>
            </div>
            <p class="mt-4 text-2xl font-bold text-white">{{ user.emailVerified ? 'Verified' : 'Pending' }}</p>
            <p class="mt-2 text-xs text-slate-500">Email verification state</p>
          </article>

          <article class="rounded-2xl border border-slate-800 bg-[#0e1420] p-5">
            <div class="flex items-center justify-between">
              <span class="text-sm text-slate-400">Two-factor authentication</span>
              <span class="text-lg text-violet-300">⬡</span>
            </div>
            <p class="mt-4 text-2xl font-bold text-white">{{ user.twoFactorEnabled ? 'Enabled' : 'Disabled' }}</p>
            <p class="mt-2 text-xs text-slate-500">Demo security setting</p>
          </article>
        </section>

        <div class="grid grid-cols-1 items-start gap-6 xl:grid-cols-3">
          <!-- Account information -->
          <section class="overflow-hidden rounded-2xl border border-slate-800 bg-[#0e1420] xl:col-span-2">
            <header class="border-b border-slate-800 px-5 py-5 sm:px-6">
              <h2 class="font-bold text-white">Account information</h2>
              <p class="mt-1 text-xs text-slate-500">Personal details and account preferences.</p>
            </header>

            <div class="grid grid-cols-1 gap-x-8 gap-y-6 p-5 sm:grid-cols-2 sm:p-6">
              <div>
                <p class="text-xs text-slate-500">Full name</p>
                <p class="mt-2 text-sm font-semibold text-slate-200">{{ user.name }}</p>
              </div>

              <div>
                <p class="text-xs text-slate-500">Email address</p>
                <p class="mt-2 break-all text-sm font-semibold text-slate-200">{{ user.email }}</p>
              </div>

              <div>
                <p class="text-xs text-slate-500">Phone number</p>
                <p class="mt-2 text-sm font-semibold text-slate-200">{{ user.phone || 'Not provided' }}</p>
              </div>

              <div>
                <p class="text-xs text-slate-500">Country</p>
                <p class="mt-2 text-sm font-semibold text-slate-200">{{ user.country || 'Not provided' }}</p>
              </div>

              <div>
                <p class="text-xs text-slate-500">Department</p>
                <p class="mt-2 text-sm font-semibold text-slate-200">{{ user.department || 'Not assigned' }}</p>
              </div>

              <div>
                <p class="text-xs text-slate-500">Favorite league</p>
                <p class="mt-2 text-sm font-semibold text-slate-200">{{ user.favoriteLeague || 'Not selected' }}</p>
              </div>

              <div>
                <p class="text-xs text-slate-500">Last login</p>
                <p class="mt-2 text-sm font-semibold text-slate-200">{{ user.lastLogin || 'No login recorded' }}</p>
              </div>

              <div>
                <p class="text-xs text-slate-500">Registration date</p>
                <p class="mt-2 text-sm font-semibold text-slate-200">{{ user.joinedAt }}</p>
              </div>

              <div class="sm:col-span-2">
                <p class="text-xs text-slate-500">About</p>
                <p class="mt-2 text-sm leading-6 text-slate-300">{{ user.bio || 'No description provided.' }}</p>
              </div>
            </div>

            <div class="border-t border-slate-800 px-5 py-4 sm:px-6">
              <button
                type="button"
                class="rounded-xl border border-slate-700 px-4 py-2.5 text-sm font-semibold text-slate-300 transition hover:border-cyan-400 hover:text-cyan-300"
                @click="openEdit"
              >
                Edit account information
              </button>
            </div>
          </section>

          <!-- Role and security -->
          <div class="space-y-6">
            <section class="rounded-2xl border border-slate-800 bg-[#0e1420] p-5 sm:p-6">
              <h2 class="font-bold text-white">Role & permissions</h2>
              <p class="mt-1 text-xs text-slate-500">Assigned access level.</p>

              <div class="mt-5 flex items-center gap-3 rounded-xl border border-cyan-400/20 bg-cyan-400/5 p-4">
                <div class="flex h-11 w-11 items-center justify-center rounded-xl bg-cyan-400/10 text-lg text-cyan-300">♙</div>
                <div>
                  <p class="font-semibold text-white">{{ user.role }}</p>
                  <p class="mt-1 text-xs text-slate-400">Assigned user role</p>
                </div>
              </div>

              <p class="mt-4 text-sm leading-6 text-slate-400">{{ roleDescription }}</p>

              <div class="mt-5 space-y-3">
                <div class="flex items-center justify-between gap-3 text-sm">
                  <span class="text-slate-400">View dashboard</span>
                  <span class="text-emerald-300">Included</span>
                </div>
                <div class="flex items-center justify-between gap-3 text-sm">
                  <span class="text-slate-400">Manage users</span>
                  <span :class="user.role === 'Admin' ? 'text-emerald-300' : 'text-slate-500'">
                    {{ user.role === 'Admin' ? 'Included' : 'Restricted' }}
                  </span>
                </div>
                <div class="flex items-center justify-between gap-3 text-sm">
                  <span class="text-slate-400">Manage settings</span>
                  <span :class="user.role === 'Admin' ? 'text-emerald-300' : 'text-slate-500'">
                    {{ user.role === 'Admin' ? 'Included' : 'Restricted' }}
                  </span>
                </div>
              </div>

              <p class="mt-4 text-xs leading-5 text-slate-600">
                Illustrative permissions only. Enforce access rules in Django.
              </p>
            </section>

            <section class="rounded-2xl border border-slate-800 bg-[#0e1420] p-5 sm:p-6">
              <h2 class="font-bold text-white">Security overview</h2>
              <p class="mt-1 text-xs text-slate-500">Account protection status.</p>

              <div class="mt-5 space-y-4">
                <div class="flex items-center justify-between gap-3">
                  <div>
                    <p class="text-sm font-medium text-slate-200">Email verified</p>
                    <p class="mt-1 text-xs text-slate-500">Email ownership status</p>
                  </div>
                  <span :class="user.emailVerified ? 'text-emerald-300' : 'text-amber-300'">
                    {{ user.emailVerified ? 'Verified' : 'Pending' }}
                  </span>
                </div>

                <div class="h-px bg-slate-800"></div>

                <div class="flex items-center justify-between gap-3">
                  <div>
                    <p class="text-sm font-medium text-slate-200">Two-factor auth</p>
                    <p class="mt-1 text-xs text-slate-500">Additional login protection</p>
                  </div>
                  <span :class="user.twoFactorEnabled ? 'text-emerald-300' : 'text-slate-500'">
                    {{ user.twoFactorEnabled ? 'Enabled' : 'Disabled' }}
                  </span>
                </div>

                <div class="h-px bg-slate-800"></div>

                <div class="flex items-center justify-between gap-3">
                  <div>
                    <p class="text-sm font-medium text-slate-200">Account state</p>
                    <p class="mt-1 text-xs text-slate-500">Current access status</p>
                  </div>
                  <span :class="user.status === 'Active' ? 'text-emerald-300' : 'text-rose-300'">
                    {{ user.status }}
                  </span>
                </div>
              </div>
            </section>
          </div>
        </div>

        <!-- Activity timeline -->
        <section class="overflow-hidden rounded-2xl border border-slate-800 bg-[#0e1420]">
          <header class="flex flex-col justify-between gap-3 border-b border-slate-800 px-5 py-5 sm:flex-row sm:items-center sm:px-6">
            <div>
              <h2 class="font-bold text-white">Recent activity</h2>
              <p class="mt-1 text-xs text-slate-500">Latest activity records available for this demo user.</p>
            </div>
            <span class="rounded-lg border border-slate-700 px-3 py-1.5 text-xs text-slate-400">
              {{ user.activities.length }} records
            </span>
          </header>

          <div v-if="user.activities.length" class="divide-y divide-slate-800/80">
            <article
              v-for="activity in user.activities"
              :key="activity.id"
              class="flex gap-4 px-5 py-5 transition hover:bg-slate-800/20 sm:px-6"
            >
              <div
                class="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl text-lg"
                :class="activityColor(activity.type)"
              >
                {{ activityIcon(activity.type) }}
              </div>
              <div class="min-w-0 flex-1">
                <div class="flex flex-col justify-between gap-1 sm:flex-row sm:items-center">
                  <h3 class="text-sm font-semibold text-white">{{ activity.action }}</h3>
                  <time class="text-xs text-slate-500">{{ activity.date }}</time>
                </div>
                <p class="mt-1 text-sm leading-6 text-slate-400">{{ activity.description }}</p>
              </div>
            </article>
          </div>

          <div v-else class="px-5 py-12 text-center text-sm text-slate-500">
            No activity records available.
          </div>
        </section>

        <!-- Danger zone -->
        <section class="rounded-2xl border border-rose-500/20 bg-rose-500/[0.03] p-5 sm:p-6">
          <div class="flex flex-col justify-between gap-5 sm:flex-row sm:items-center">
            <div>
              <h2 class="font-bold text-rose-300">Danger zone</h2>
              <p class="mt-2 max-w-2xl text-sm leading-6 text-slate-400">
                Remove this demo user from the local list. A production implementation should use a protected backend endpoint and an audit trail.
              </p>
            </div>
            <button
              type="button"
              class="shrink-0 rounded-xl border border-rose-500/40 px-4 py-2.5 text-sm font-semibold text-rose-300 transition hover:bg-rose-500/10"
              @click="showDeleteConfirm = true"
            >
              Delete user
            </button>
          </div>
        </section>
      </template>
    </div>

    <!-- Edit modal -->
    <Teleport to="body">
      <div
        v-if="showEditModal"
        class="fixed inset-0 z-50 flex items-center justify-center overflow-y-auto bg-black/75 p-4 backdrop-blur-sm"
        @click.self="showEditModal = false"
      >
        <section
          role="dialog"
          aria-modal="true"
          aria-label="Edit user"
          class="my-auto max-h-[92vh] w-full max-w-2xl overflow-y-auto rounded-2xl border border-slate-700 bg-[#0e1420]"
        >
          <header class="flex items-center justify-between border-b border-slate-800 px-6 py-5">
            <div>
              <h2 class="text-lg font-bold text-white">Edit user</h2>
              <p class="mt-1 text-xs text-slate-500">Update the user's demo profile.</p>
            </div>
            <button type="button" class="rounded-lg p-2 text-slate-400 hover:bg-slate-800" @click="showEditModal = false">
              ✕
            </button>
          </header>

          <form class="space-y-5 p-6" @submit.prevent="saveEdit">
            <div v-if="formError" class="rounded-xl border border-rose-500/30 bg-rose-500/10 px-4 py-3 text-sm text-rose-300" role="alert">
              {{ formError }}
            </div>

            <div class="grid grid-cols-1 gap-5 sm:grid-cols-2">
              <label class="block">
                <span class="mb-2 block text-sm text-slate-300">Full name *</span>
                <input v-model="editForm.name" required maxlength="120" class="w-full rounded-xl border border-slate-700 bg-[#090d16] px-4 py-3 text-sm text-white outline-none focus:border-cyan-400" />
              </label>

              <label class="block">
                <span class="mb-2 block text-sm text-slate-300">Email *</span>
                <input v-model="editForm.email" required type="email" maxlength="254" class="w-full rounded-xl border border-slate-700 bg-[#090d16] px-4 py-3 text-sm text-white outline-none focus:border-cyan-400" />
              </label>

              <label class="block">
                <span class="mb-2 block text-sm text-slate-300">Phone</span>
                <input v-model="editForm.phone" type="tel" maxlength="30" class="w-full rounded-xl border border-slate-700 bg-[#090d16] px-4 py-3 text-sm text-white outline-none focus:border-cyan-400" />
              </label>

              <label class="block">
                <span class="mb-2 block text-sm text-slate-300">Country</span>
                <input v-model="editForm.country" maxlength="80" class="w-full rounded-xl border border-slate-700 bg-[#090d16] px-4 py-3 text-sm text-white outline-none focus:border-cyan-400" />
              </label>

              <label class="block">
                <span class="mb-2 block text-sm text-slate-300">Role</span>
                <select v-model="editForm.role" class="w-full rounded-xl border border-slate-700 bg-[#090d16] px-4 py-3 text-sm text-white outline-none focus:border-cyan-400">
                  <option value="Admin">Admin</option>
                  <option value="Analyst">Analyst</option>
                  <option value="Scout">Scout</option>
                  <option value="User">User</option>
                </select>
              </label>

              <label class="block">
                <span class="mb-2 block text-sm text-slate-300">Department</span>
                <input v-model="editForm.department" maxlength="100" class="w-full rounded-xl border border-slate-700 bg-[#090d16] px-4 py-3 text-sm text-white outline-none focus:border-cyan-400" />
              </label>

              <label class="block sm:col-span-2">
                <span class="mb-2 block text-sm text-slate-300">Favorite league</span>
                <select v-model="editForm.favoriteLeague" class="w-full rounded-xl border border-slate-700 bg-[#090d16] px-4 py-3 text-sm text-white outline-none focus:border-cyan-400">
                  <option value="">None selected</option>
                  <option>Premier League</option>
                  <option>La Liga</option>
                  <option>Bundesliga</option>
                  <option>Serie A</option>
                  <option>Ligue 1</option>
                  <option>Egyptian Premier League</option>
                </select>
              </label>

              <label class="block sm:col-span-2">
                <span class="mb-2 block text-sm text-slate-300">About</span>
                <textarea v-model="editForm.bio" rows="3" maxlength="500" class="w-full resize-y rounded-xl border border-slate-700 bg-[#090d16] px-4 py-3 text-sm text-white outline-none focus:border-cyan-400"></textarea>
              </label>
            </div>

            <footer class="flex flex-col-reverse gap-3 border-t border-slate-800 pt-5 sm:flex-row sm:justify-end">
              <button type="button" class="rounded-xl border border-slate-700 px-5 py-3 text-sm font-semibold text-slate-300 hover:bg-slate-800" @click="showEditModal = false">
                Cancel
              </button>
              <button type="submit" class="rounded-xl bg-cyan-400 px-5 py-3 text-sm font-bold text-slate-950 hover:bg-cyan-300">
                Save changes
              </button>
            </footer>
          </form>
        </section>
      </div>
    </Teleport>

    <!-- Status confirmation -->
    <Teleport to="body">
      <div v-if="showStatusConfirm && user" class="fixed inset-0 z-50 flex items-center justify-center bg-black/75 p-4 backdrop-blur-sm" @click.self="showStatusConfirm = false">
        <section role="alertdialog" aria-modal="true" class="w-full max-w-md rounded-2xl border border-slate-700 bg-[#0e1420] p-6">
          <h2 class="text-lg font-bold text-white">
            {{ user.status === 'Active' ? 'Suspend this account?' : 'Activate this account?' }}
          </h2>
          <p class="mt-3 text-sm leading-6 text-slate-400">
            This changes the account status in the current demo session only. It does not revoke tokens or change Django access.
          </p>
          <div class="mt-6 flex justify-end gap-3">
            <button type="button" class="rounded-xl border border-slate-700 px-4 py-2.5 text-sm text-slate-300 hover:bg-slate-800" @click="showStatusConfirm = false">
              Cancel
            </button>
            <button type="button" class="rounded-xl bg-cyan-400 px-4 py-2.5 text-sm font-bold text-slate-950 hover:bg-cyan-300" @click="toggleStatus">
              Confirm
            </button>
          </div>
        </section>
      </div>
    </Teleport>

    <!-- Delete confirmation -->
    <Teleport to="body">
      <div v-if="showDeleteConfirm && user" class="fixed inset-0 z-[60] flex items-center justify-center bg-black/75 p-4 backdrop-blur-sm" @click.self="showDeleteConfirm = false">
        <section role="alertdialog" aria-modal="true" class="w-full max-w-md rounded-2xl border border-rose-500/30 bg-[#0e1420] p-6">
          <div class="flex h-12 w-12 items-center justify-center rounded-xl bg-rose-500/10 text-xl text-rose-300">!</div>
          <h2 class="mt-4 text-lg font-bold text-white">Delete {{ user.name }}?</h2>
          <p class="mt-2 text-sm leading-6 text-slate-400">
            This removes the selected user from the demo list. It does not delete a real account from the database.
          </p>
          <div class="mt-6 flex justify-end gap-3">
            <button type="button" class="rounded-xl border border-slate-700 px-4 py-2.5 text-sm text-slate-300 hover:bg-slate-800" @click="showDeleteConfirm = false">
              Cancel
            </button>
            <button type="button" class="rounded-xl bg-rose-500 px-4 py-2.5 text-sm font-bold text-white hover:bg-rose-400" @click="deleteUser">
              Delete user
            </button>
          </div>
        </section>
      </div>
    </Teleport>
  </div>
</template>
