
<script setup lang="ts">
import { computed, ref } from 'vue'

interface Profile {
  name: string
  email: string
  phone: string
  jobTitle: string
  location: string
  bio: string
  role: string
}

const profile = ref<Profile>({
  name: 'Diaa Mohamed',
  email: 'diaamazize98@gmail.com',
  phone: '',
  jobTitle: 'Software Engineer',
  location: 'Cairo, Egypt',
  bio: 'Software engineer interested in full-stack development and AI-powered applications.',
  role: 'Administrator',
})

const form = ref<Profile>({ ...profile.value })
const editing = ref(false)
const showPasswordForm = ref(false)
const currentPassword = ref('')
const newPassword = ref('')
const confirmPassword = ref('')
const message = ref('')
const messageType = ref<'success' | 'error'>('success')

const initials = computed(() =>
  profile.value.name
    .trim()
    .split(/\s+/)
    .slice(0, 2)
    .map(part => part[0]?.toUpperCase() ?? '')
    .join(''),
)

function notify(text: string, type: 'success' | 'error' = 'success') {
  message.value = text
  messageType.value = type
}

function startEditing() {
  form.value = { ...profile.value }
  editing.value = true
  message.value = ''
}

function saveProfile() {
  if (!form.value.name.trim() || !form.value.email.trim()) {
    notify('Name and email are required.', 'error')
    return
  }

  profile.value = { ...form.value }
  editing.value = false
  notify('Profile updated successfully.')
}

function changePassword() {
  if (!currentPassword.value || !newPassword.value || !confirmPassword.value) {
    notify('Please complete all password fields.', 'error')
    return
  }

  if (newPassword.value.length < 8) {
    notify('The new password must contain at least 8 characters.', 'error')
    return
  }

  if (newPassword.value !== confirmPassword.value) {
    notify('The passwords do not match.', 'error')
    return
  }

  // Demo only: connect this action to your backend password endpoint.
  currentPassword.value = ''
  newPassword.value = ''
  confirmPassword.value = ''
  showPasswordForm.value = false
  notify('Demo validation completed. Connect the backend to change your password.')
}

const activities = [
  { title: 'Profile viewed', description: 'You opened your profile settings.', time: 'Just now' },
  { title: 'Account active', description: 'Your account is currently active.', time: 'Today' },
  { title: 'Security check', description: 'Review your password and account security.', time: 'Recommended' },
]
</script>

<template>
  <div class="min-h-screen bg-slate-950 p-4 text-slate-100 sm:p-6 lg:p-8">
    <div class="mx-auto max-w-6xl space-y-6">
      <header class="flex flex-wrap items-center justify-between gap-4">
        <div>
          <p class="text-sm font-medium text-cyan-400">ACCOUNT MANAGEMENT</p>
          <h1 class="mt-2 text-3xl font-bold tracking-tight">My Profile</h1>
          <p class="mt-2 text-sm text-slate-400">
            Manage your personal information and account security.
          </p>
        </div>

        <button
          v-if="!editing"
          class="rounded-xl bg-cyan-500 px-5 py-3 text-sm font-semibold text-slate-950 transition hover:bg-cyan-400"
          @click="startEditing"
        >
          Edit profile
        </button>
      </header>

      <div
        v-if="message"
        class="rounded-xl border px-4 py-3 text-sm"
        :class="messageType === 'error'
          ? 'border-rose-500/30 bg-rose-500/10 text-rose-300'
          : 'border-emerald-500/30 bg-emerald-500/10 text-emerald-300'"
      >
        {{ message }}
      </div>

      <section class="overflow-hidden rounded-2xl border border-slate-800 bg-slate-900">
        <div class="h-36 bg-gradient-to-r from-cyan-950 via-blue-900 to-indigo-950"></div>

        <div class="flex flex-col gap-5 px-6 pb-6 sm:flex-row sm:items-end sm:justify-between">
          <div class="-mt-12 flex items-end gap-4">
            <div
              class="flex h-24 w-24 shrink-0 items-center justify-center rounded-2xl border-4 border-slate-900 bg-cyan-500 text-2xl font-bold text-slate-950 shadow-xl"
            >
              {{ initials }}
            </div>

            <div class="pb-1">
              <h2 class="text-xl font-bold">{{ profile.name }}</h2>
              <p class="mt-1 text-sm text-slate-400">{{ profile.jobTitle }}</p>
            </div>
          </div>

          <div class="flex flex-wrap items-center gap-2 sm:pb-1">
            <span class="rounded-full border border-emerald-500/20 bg-emerald-500/10 px-3 py-1.5 text-xs font-semibold text-emerald-300">
              ● Active account
            </span>
            <span class="rounded-full border border-cyan-500/20 bg-cyan-500/10 px-3 py-1.5 text-xs font-semibold text-cyan-300">
              {{ profile.role }}
            </span>
          </div>
        </div>
      </section>

      <div class="grid gap-6 lg:grid-cols-[1.5fr_1fr]">
        <section class="rounded-2xl border border-slate-800 bg-slate-900 p-6">
          <div class="mb-6 flex items-center justify-between">
            <div>
              <h2 class="text-lg font-semibold">Personal information</h2>
              <p class="mt-1 text-sm text-slate-400">Your basic account details</p>
            </div>
            <span class="text-xl text-cyan-400">◎</span>
          </div>

          <form v-if="editing" class="space-y-4" @submit.prevent="saveProfile">
            <div class="grid gap-4 sm:grid-cols-2">
              <label class="block text-sm text-slate-300">
                Full name
                <input
                  v-model="form.name"
                  required
                  class="mt-2 w-full rounded-xl border border-slate-700 bg-slate-950 px-4 py-3 text-white outline-none focus:border-cyan-500"
                />
              </label>

              <label class="block text-sm text-slate-300">
                Email address
                <input
                  v-model="form.email"
                  required
                  type="email"
                  class="mt-2 w-full rounded-xl border border-slate-700 bg-slate-950 px-4 py-3 text-white outline-none focus:border-cyan-500"
                />
              </label>

              <label class="block text-sm text-slate-300">
                Phone number
                <input
                  v-model="form.phone"
                  type="tel"
                  class="mt-2 w-full rounded-xl border border-slate-700 bg-slate-950 px-4 py-3 text-white outline-none focus:border-cyan-500"
                />
              </label>

              <label class="block text-sm text-slate-300">
                Job title
                <input
                  v-model="form.jobTitle"
                  class="mt-2 w-full rounded-xl border border-slate-700 bg-slate-950 px-4 py-3 text-white outline-none focus:border-cyan-500"
                />
              </label>

              <label class="block text-sm text-slate-300 sm:col-span-2">
                Location
                <input
                  v-model="form.location"
                  class="mt-2 w-full rounded-xl border border-slate-700 bg-slate-950 px-4 py-3 text-white outline-none focus:border-cyan-500"
                />
              </label>

              <label class="block text-sm text-slate-300 sm:col-span-2">
                About me
                <textarea
                  v-model="form.bio"
                  rows="4"
                  class="mt-2 w-full resize-y rounded-xl border border-slate-700 bg-slate-950 px-4 py-3 text-white outline-none focus:border-cyan-500"
                ></textarea>
              </label>
            </div>

            <div class="flex flex-wrap gap-3 pt-2">
              <button
                type="submit"
                class="rounded-xl bg-cyan-500 px-5 py-3 text-sm font-semibold text-slate-950 hover:bg-cyan-400"
              >
                Save changes
              </button>
              <button
                type="button"
                class="rounded-xl border border-slate-700 px-5 py-3 text-sm font-medium text-slate-300 hover:bg-slate-800"
                @click="editing = false; message = ''"
              >
                Cancel
              </button>
            </div>
          </form>

          <div v-else class="grid gap-5 sm:grid-cols-2">
            <div>
              <p class="text-xs uppercase tracking-wider text-slate-500">Full name</p>
              <p class="mt-2 font-medium">{{ profile.name }}</p>
            </div>
            <div>
              <p class="text-xs uppercase tracking-wider text-slate-500">Email address</p>
              <p class="mt-2 break-all font-medium">{{ profile.email }}</p>
            </div>
            <div>
              <p class="text-xs uppercase tracking-wider text-slate-500">Phone number</p>
              <p class="mt-2 font-medium">{{ profile.phone || 'Not provided' }}</p>
            </div>
            <div>
              <p class="text-xs uppercase tracking-wider text-slate-500">Job title</p>
              <p class="mt-2 font-medium">{{ profile.jobTitle || 'Not provided' }}</p>
            </div>
            <div>
              <p class="text-xs uppercase tracking-wider text-slate-500">Location</p>
              <p class="mt-2 font-medium">{{ profile.location || 'Not provided' }}</p>
            </div>
            <div>
              <p class="text-xs uppercase tracking-wider text-slate-500">Account role</p>
              <p class="mt-2 font-medium">{{ profile.role }}</p>
            </div>
            <div class="sm:col-span-2">
              <p class="text-xs uppercase tracking-wider text-slate-500">About me</p>
              <p class="mt-2 text-sm leading-6 text-slate-300">
                {{ profile.bio || 'No description added yet.' }}
              </p>
            </div>
          </div>
        </section>

        <div class="space-y-6">
          <section class="rounded-2xl border border-slate-800 bg-slate-900 p-6">
            <h2 class="text-lg font-semibold">Account security</h2>
            <p class="mt-1 text-sm text-slate-400">Keep your account protected.</p>

            <div class="mt-5 flex items-center justify-between gap-3 rounded-xl border border-slate-800 bg-slate-950 p-4">
              <div>
                <p class="font-medium">Password</p>
                <p class="mt-1 text-xs text-slate-500">Update your account password</p>
              </div>
              <button
                class="shrink-0 rounded-lg border border-slate-700 px-3 py-2 text-xs font-semibold hover:border-cyan-500"
                @click="showPasswordForm = !showPasswordForm"
              >
                {{ showPasswordForm ? 'Cancel' : 'Change' }}
              </button>
            </div>

            <form v-if="showPasswordForm" class="mt-4 space-y-3" @submit.prevent="changePassword">
              <input
                v-model="currentPassword"
                type="password"
                autocomplete="current-password"
                placeholder="Current password"
                class="w-full rounded-xl border border-slate-700 bg-slate-950 px-4 py-3 text-sm outline-none focus:border-cyan-500"
              />
              <input
                v-model="newPassword"
                type="password"
                autocomplete="new-password"
                placeholder="New password (8+ characters)"
                class="w-full rounded-xl border border-slate-700 bg-slate-950 px-4 py-3 text-sm outline-none focus:border-cyan-500"
              />
              <input
                v-model="confirmPassword"
                type="password"
                autocomplete="new-password"
                placeholder="Confirm new password"
                class="w-full rounded-xl border border-slate-700 bg-slate-950 px-4 py-3 text-sm outline-none focus:border-cyan-500"
              />
              <button
                type="submit"
                class="w-full rounded-xl bg-cyan-500 px-4 py-3 text-sm font-semibold text-slate-950 hover:bg-cyan-400"
              >
                Update password
              </button>
              <p class="text-xs leading-5 text-amber-300">
                Demo form only. A secure backend endpoint is required to change your real password.
              </p>
            </form>

            <div class="mt-4 flex items-start gap-3 rounded-xl bg-emerald-500/5 p-4">
              <span class="mt-0.5 text-emerald-400">✓</span>
              <div>
                <p class="text-sm font-medium">Account status</p>
                <p class="mt-1 text-xs leading-5 text-slate-400">
                  Your account is marked as active in this demo.
                </p>
              </div>
            </div>
          </section>

          <section class="rounded-2xl border border-slate-800 bg-slate-900 p-6">
            <h2 class="text-lg font-semibold">Recent activity</h2>
            <div class="mt-5 space-y-5">
              <div v-for="activity in activities" :key="activity.title" class="flex gap-3">
                <div class="mt-1 h-2.5 w-2.5 shrink-0 rounded-full bg-cyan-400"></div>
                <div class="min-w-0 flex-1">
                  <div class="flex flex-wrap justify-between gap-2">
                    <p class="text-sm font-medium">{{ activity.title }}</p>
                    <span class="text-xs text-slate-500">{{ activity.time }}</span>
                  </div>
                  <p class="mt-1 text-xs leading-5 text-slate-400">{{ activity.description }}</p>
                </div>
              </div>
            </div>
          </section>
        </div>
      </div>

      <p class="text-center text-xs text-slate-600">
        FIDS · Football Intelligence Decision System
      </p>
    </div>
  </div>
</template>