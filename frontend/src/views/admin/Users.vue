
<script setup lang="ts">
import { computed, onMounted, reactive, ref } from 'vue'

type UserRole = 'admin' | 'analyst' | 'scout' | 'user'

interface AppUser {
  id: number
  username: string
  email: string
  first_name: string
  last_name: string
  role: UserRole
  is_active: boolean
}

interface UserForm {
  username: string
  email: string
  first_name: string
  last_name: string
  role: UserRole
  is_active: boolean
  password: string
}

const API_BASE_URL = (
  import.meta.env.VITE_API_BASE_URL ||
  'http://127.0.0.1:8000/api/v1'
).replace(/\/+$/, '')

const USERS_ENDPOINT = `${API_BASE_URL}/auth/admin/users/`

const users = ref<AppUser[]>([])
const loading = ref(false)
const saving = ref(false)
const searchQuery = ref('')
const roleFilter = ref('all')
const statusFilter = ref('all')
const showModal = ref(false)
const editingUserId = ref<number | null>(null)
const errorMessage = ref('')
const successMessage = ref('')
const formError = ref('')

const emptyForm = (): UserForm => ({
  username: '',
  email: '',
  first_name: '',
  last_name: '',
  role: 'user',
  is_active: true,
  password: '',
})

const form = reactive<UserForm>(emptyForm())

const accessToken = () => {
  return (
    localStorage.getItem('fids_access_token') ||
    localStorage.getItem('access') ||
    localStorage.getItem('access_token') ||
    localStorage.getItem('accessToken') ||
    sessionStorage.getItem('fids_access_token') ||
    ''
  )
}

async function apiRequest(
  url: string,
  options: RequestInit = {},
): Promise<any> {
  const token = accessToken()

  const headers = new Headers(options.headers)
  headers.set('Accept', 'application/json')

  if (options.body) {
    headers.set('Content-Type', 'application/json')
  }

  if (token) {
    headers.set('Authorization', `Bearer ${token}`)
  }

  const response = await fetch(url, {
    ...options,
    headers,
  })

  const text = await response.text()
  let data: any = null

  if (text) {
    try {
      data = JSON.parse(text)
    } catch {
      data = { detail: text }
    }
  }

  if (!response.ok) {
    const detail =
      data?.detail ||
      data?.message ||
      (typeof data === 'object' ? JSON.stringify(data) : '') ||
      `Request failed (${response.status})`

    if (response.status === 401) {
      throw new Error('انتهت جلسة تسجيل الدخول أو أن التوكن غير صالح. سجّل الدخول مرة أخرى.')
    }

    if (response.status === 403) {
      throw new Error('ليس لديك صلاحية إدارة المستخدمين.')
    }

    if (response.status === 404) {
      throw new Error('لم يتم العثور على المسار المطلوب. راجع Django URLs.')
    }

    if (response.status === 405) {
      throw new Error('العملية غير مدعومة في الـ Backend.')
    }

    throw new Error(
      typeof detail === 'string' ? detail : JSON.stringify(detail),
    )
  }

  return data
}

function normalizeRole(value: unknown): UserRole {
  const role = String(value ?? 'user').toLowerCase()

  if (role === 'admin') return 'admin'
  if (role === 'analyst') return 'analyst'
  if (role === 'scout') return 'scout'

  return 'user'
}

function mapApiUser(raw: any): AppUser {
  return {
    id: Number(raw.id),
    username: String(raw.username ?? ''),
    email: String(raw.email ?? ''),
    first_name: String(raw.first_name ?? ''),
    last_name: String(raw.last_name ?? ''),
    role: normalizeRole(raw.role),
    is_active: Boolean(raw.is_active),
  }
}

const filteredUsers = computed(() => {
  const query = searchQuery.value.trim().toLowerCase()

  return users.value.filter((user) => {
    const matchesSearch =
      !query ||
      user.username.toLowerCase().includes(query) ||
      user.email.toLowerCase().includes(query) ||
      `${user.first_name} ${user.last_name}`.toLowerCase().includes(query)

    const matchesRole =
      roleFilter.value === 'all' || user.role === roleFilter.value

    const matchesStatus =
      statusFilter.value === 'all' ||
      (statusFilter.value === 'active' && user.is_active) ||
      (statusFilter.value === 'inactive' && !user.is_active)

    return matchesSearch && matchesRole && matchesStatus
  })
})

const totalUsers = computed(() => users.value.length)
const activeUsers = computed(
  () => users.value.filter((user) => user.is_active).length,
)
const inactiveUsers = computed(
  () => users.value.filter((user) => !user.is_active).length,
)
const adminUsers = computed(
  () => users.value.filter((user) => user.role === 'admin').length,
)

function getErrorMessage(error: unknown): string {
  return error instanceof Error
    ? error.message
    : 'حدث خطأ غير متوقع. حاول مرة أخرى.'
}

async function loadUsers() {
  loading.value = true
  errorMessage.value = ''

  try {
    const data = await apiRequest(USERS_ENDPOINT)

    const records = Array.isArray(data)
      ? data
      : Array.isArray(data?.results)
        ? data.results
        : null

    if (!records) {
      throw new Error('استجابة المستخدمين من الـ API غير متوقعة.')
    }

    users.value = records.map(mapApiUser)
  } catch (error) {
    errorMessage.value = getErrorMessage(error)
  } finally {
    loading.value = false
  }
}

function openCreateModal() {
  editingUserId.value = null
  Object.assign(form, emptyForm())
  formError.value = ''
  successMessage.value = ''
  showModal.value = true
}

function openEditModal(user: AppUser) {
  editingUserId.value = user.id

  Object.assign(form, {
    username: user.username,
    email: user.email,
    first_name: user.first_name,
    last_name: user.last_name,
    role: user.role,
    is_active: user.is_active,
    password: '',
  })

  formError.value = ''
  successMessage.value = ''
  showModal.value = true
}

function closeModal() {
  if (saving.value) return
  showModal.value = false
}

async function saveUser() {
  formError.value = ''
  successMessage.value = ''

  if (!form.username.trim() || !form.email.trim()) {
    formError.value = 'اسم المستخدم والبريد الإلكتروني مطلوبان.'
    return
  }

  if (!editingUserId.value && form.password.length < 8) {
    formError.value = 'كلمة المرور مطلوبة ويجب ألا تقل عن 8 أحرف.'
    return
  }

  saving.value = true

  const payload: Record<string, unknown> = {
    username: form.username.trim(),
    email: form.email.trim().toLowerCase(),
    first_name: form.first_name.trim(),
    last_name: form.last_name.trim(),
    role: form.role,
    is_active: form.is_active,
  }

  if (form.password) {
    payload.password = form.password
  }

  try {
    if (editingUserId.value !== null) {
      await apiRequest(
        `${USERS_ENDPOINT}${editingUserId.value}/`,
        {
          method: 'PATCH',
          body: JSON.stringify(payload),
        },
      )

      successMessage.value = 'تم تحديث المستخدم بنجاح.'
    } else {
      payload.password = form.password

      await apiRequest(USERS_ENDPOINT, {
        method: 'POST',
        body: JSON.stringify(payload),
      })

      successMessage.value = 'تم إنشاء المستخدم بنجاح.'
    }

    showModal.value = false
    await loadUsers()
  } catch (error) {
    formError.value = getErrorMessage(error)
  } finally {
    saving.value = false
  }
}

async function toggleStatus(user: AppUser) {
  const nextStatus = !user.is_active
  const action = nextStatus ? 'تفعيل' : 'تعطيل'

  if (!window.confirm(`هل تريد ${action} حساب ${user.username}؟`)) {
    return
  }

  errorMessage.value = ''
  successMessage.value = ''

  try {
    await apiRequest(`${USERS_ENDPOINT}${user.id}/`, {
      method: 'PATCH',
      body: JSON.stringify({ is_active: nextStatus }),
    })

    successMessage.value = nextStatus
      ? 'تم تفعيل الحساب بنجاح.'
      : 'تم تعطيل الحساب بنجاح.'

    await loadUsers()
  } catch (error) {
    errorMessage.value = getErrorMessage(error)
  }
}

async function deleteUser(user: AppUser) {
  const confirmed = window.confirm(
    `هل أنت متأكد من حذف المستخدم "${user.username}"؟ لا يمكن التراجع عن هذا الإجراء.`,
  )

  if (!confirmed) return

  errorMessage.value = ''
  successMessage.value = ''

  try {
    await apiRequest(`${USERS_ENDPOINT}${user.id}/`, {
      method: 'DELETE',
    })

    users.value = users.value.filter((item) => item.id !== user.id)
    successMessage.value = 'تم حذف المستخدم بنجاح.'
  } catch (error) {
    errorMessage.value = getErrorMessage(error)
  }
}

function roleLabel(role: UserRole): string {
  const labels: Record<UserRole, string> = {
    admin: 'Admin',
    analyst: 'Analyst',
    scout: 'Scout',
    user: 'User',
  }

  return labels[role]
}

onMounted(loadUsers)
</script>

<template>
  <main class="min-h-screen bg-[#070A0F] p-4 text-white sm:p-6 lg:p-8">
    <div class="mx-auto max-w-7xl space-y-7">

      <!-- Header -->
      <header class="flex flex-col justify-between gap-5 sm:flex-row sm:items-center">
        <div>
          <p class="mb-2 text-xs font-semibold uppercase tracking-[0.25em] text-[#B7FF3C]">
            FIDS / ADMINISTRATION
          </p>
          <h1 class="text-3xl font-bold tracking-tight sm:text-4xl">
            Users Management
          </h1>
          <p class="mt-2 text-sm text-gray-400">
            Manage accounts, roles and access to the platform.
          </p>
        </div>

        <div class="flex flex-wrap gap-3">
          <button
            type="button"
            @click="loadUsers"
            :disabled="loading"
            class="rounded-xl border border-white/10 bg-[#0F141C] px-4 py-3 text-sm font-medium text-gray-200 transition hover:border-[#B7FF3C]/50 disabled:opacity-50"
          >
            {{ loading ? 'Loading...' : '↻ Refresh' }}
          </button>

          <button
            type="button"
            @click="openCreateModal"
            class="rounded-xl bg-[#B7FF3C] px-5 py-3 text-sm font-bold text-black transition hover:bg-[#caff65]"
          >
            + Add User
          </button>
        </div>
      </header>

      <!-- Notifications -->
      <div
        v-if="errorMessage"
        role="alert"
        class="flex items-start justify-between gap-3 rounded-xl border border-red-500/30 bg-red-500/10 p-4 text-sm text-red-300"
      >
        <span>{{ errorMessage }}</span>
        <button type="button" @click="errorMessage = ''" aria-label="Dismiss error">✕</button>
      </div>

      <div
        v-if="successMessage"
        role="status"
        class="flex items-start justify-between gap-3 rounded-xl border border-[#B7FF3C]/20 bg-[#B7FF3C]/10 p-4 text-sm text-[#B7FF3C]"
      >
        <span>{{ successMessage }}</span>
        <button type="button" @click="successMessage = ''" aria-label="Dismiss message">✕</button>
      </div>

      <!-- Statistics -->
      <section class="grid grid-cols-1 gap-4 sm:grid-cols-2 xl:grid-cols-4">
        <article class="rounded-2xl border border-white/[0.07] bg-[#0F141C] p-5">
          <p class="text-sm text-gray-400">Total Users</p>
          <div class="mt-4 flex items-end justify-between">
            <p class="text-3xl font-bold">{{ totalUsers }}</p>
            <span class="text-xl text-[#B7FF3C]">♙</span>
          </div>
        </article>

        <article class="rounded-2xl border border-white/[0.07] bg-[#0F141C] p-5">
          <p class="text-sm text-gray-400">Active Accounts</p>
          <div class="mt-4 flex items-end justify-between">
            <p class="text-3xl font-bold">{{ activeUsers }}</p>
            <span class="text-xl text-[#B7FF3C]">✓</span>
          </div>
        </article>

        <article class="rounded-2xl border border-white/[0.07] bg-[#0F141C] p-5">
          <p class="text-sm text-gray-400">Administrators</p>
          <div class="mt-4 flex items-end justify-between">
            <p class="text-3xl font-bold">{{ adminUsers }}</p>
            <span class="text-xl text-[#B7FF3C]">♜</span>
          </div>
        </article>

        <article class="rounded-2xl border border-white/[0.07] bg-[#0F141C] p-5">
          <p class="text-sm text-gray-400">Inactive Accounts</p>
          <div class="mt-4 flex items-end justify-between">
            <p class="text-3xl font-bold">{{ inactiveUsers }}</p>
            <span class="text-xl text-amber-400">◷</span>
          </div>
        </article>
      </section>

      <!-- Users table -->
      <section class="overflow-hidden rounded-2xl border border-white/[0.07] bg-[#0F141C]">
        <div class="flex flex-col gap-4 border-b border-white/[0.07] p-5 lg:flex-row lg:items-center lg:justify-between">
          <div>
            <h2 class="text-lg font-semibold">Platform Users</h2>
            <p class="mt-1 text-sm text-gray-500">
              Showing {{ filteredUsers.length }} of {{ totalUsers }} users
            </p>
          </div>

          <div class="grid grid-cols-1 gap-3 sm:grid-cols-3">
            <input
              v-model="searchQuery"
              type="search"
              placeholder="Search users..."
              class="min-w-0 rounded-xl border border-white/10 bg-[#070A0F] px-4 py-3 text-sm outline-none transition placeholder:text-gray-600 focus:border-[#B7FF3C]/60"
            />

            <select
              v-model="roleFilter"
              class="rounded-xl border border-white/10 bg-[#070A0F] px-3 py-3 text-sm text-gray-300 outline-none focus:border-[#B7FF3C]/60"
            >
              <option value="all">All roles</option>
              <option value="admin">Admin</option>
              <option value="analyst">Analyst</option>
              <option value="scout">Scout</option>
              <option value="user">User</option>
            </select>

            <select
              v-model="statusFilter"
              class="rounded-xl border border-white/10 bg-[#070A0F] px-3 py-3 text-sm text-gray-300 outline-none focus:border-[#B7FF3C]/60"
            >
              <option value="all">All statuses</option>
              <option value="active">Active</option>
              <option value="inactive">Inactive</option>
            </select>
          </div>
        </div>

        <div v-if="loading && users.length === 0" class="p-12 text-center text-sm text-gray-400">
          Loading users from the server...
        </div>

        <div v-else-if="!loading && filteredUsers.length === 0" class="p-12 text-center">
          <p class="text-lg font-semibold text-gray-300">No users found</p>
          <p class="mt-2 text-sm text-gray-500">
            Try another search or create a new user.
          </p>
        </div>

        <div v-else class="overflow-x-auto">
          <table class="w-full min-w-[850px] text-left text-sm">
            <thead class="bg-white/[0.025] text-xs uppercase tracking-wider text-gray-500">
              <tr>
                <th class="px-5 py-4 font-medium">User</th>
                <th class="px-5 py-4 font-medium">Role</th>
                <th class="px-5 py-4 font-medium">Status</th>
                <th class="px-5 py-4 text-right font-medium">Actions</th>
              </tr>
            </thead>

            <tbody class="divide-y divide-white/[0.06]">
              <tr
                v-for="user in filteredUsers"
                :key="user.id"
                class="transition hover:bg-white/[0.025]"
              >
                <td class="px-5 py-4">
                  <div class="flex items-center gap-3">
                    <div class="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-[#B7FF3C]/10 text-sm font-bold text-[#B7FF3C]">
                      {{ (user.first_name || user.username).charAt(0).toUpperCase() }}
                    </div>

                    <div>
                      <p class="font-semibold text-gray-100">
                        {{ `${user.first_name} ${user.last_name}`.trim() || user.username }}
                      </p>
                      <p class="mt-1 text-xs text-gray-500">
                        @{{ user.username }} · {{ user.email }}
                      </p>
                    </div>
                  </div>
                </td>

                <td class="px-5 py-4">
                  <span
                    class="inline-flex rounded-lg border border-white/10 bg-white/[0.04] px-3 py-1.5 text-xs font-medium text-gray-300"
                  >
                    {{ roleLabel(user.role) }}
                  </span>
                </td>

                <td class="px-5 py-4">
                  <span
                    class="inline-flex items-center gap-2 rounded-full px-3 py-1.5 text-xs font-medium"
                    :class="user.is_active
                      ? 'bg-[#B7FF3C]/10 text-[#B7FF3C]'
                      : 'bg-gray-500/15 text-gray-400'"
                  >
                    <span
                      class="h-1.5 w-1.5 rounded-full"
                      :class="user.is_active ? 'bg-[#B7FF3C]' : 'bg-gray-500'"
                    ></span>
                    {{ user.is_active ? 'Active' : 'Inactive' }}
                  </span>
                </td>

                <td class="px-5 py-4">
                  <div class="flex justify-end gap-2">
                    <button
                      type="button"
                      @click="openEditModal(user)"
                      class="rounded-lg border border-white/10 px-3 py-2 text-xs text-gray-300 transition hover:border-[#B7FF3C]/40 hover:text-[#B7FF3C]"
                    >
                      Edit
                    </button>

                    <button
                      type="button"
                      @click="toggleStatus(user)"
                      class="rounded-lg border border-white/10 px-3 py-2 text-xs text-gray-300 transition hover:border-amber-400/40 hover:text-amber-300"
                    >
                      {{ user.is_active ? 'Disable' : 'Activate' }}
                    </button>

                    <button
                      type="button"
                      @click="deleteUser(user)"
                      class="rounded-lg border border-red-500/20 px-3 py-2 text-xs text-red-300 transition hover:bg-red-500/10"
                    >
                      Delete
                    </button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <div class="border-t border-white/[0.07] px-5 py-4 text-xs text-gray-500">
          FIDS User Administration
        </div>
      </section>
    </div>

    <!-- Create / Edit modal -->
    <Teleport to="body">
      <div
        v-if="showModal"
        class="fixed inset-0 z-50 flex items-center justify-center overflow-y-auto bg-black/75 p-4 backdrop-blur-sm"
        @click.self="closeModal"
        @keydown.esc="closeModal"
      >
        <section
          role="dialog"
          aria-modal="true"
          aria-labelledby="user-modal-title"
          class="my-auto w-full max-w-2xl rounded-2xl border border-white/10 bg-[#0F141C] shadow-2xl"
        >
          <header class="flex items-start justify-between border-b border-white/[0.07] p-6">
            <div>
              <p class="text-xs font-semibold uppercase tracking-[0.2em] text-[#B7FF3C]">
                USER MANAGEMENT
              </p>
              <h2 id="user-modal-title" class="mt-2 text-xl font-bold">
                {{ editingUserId !== null ? 'Edit User' : 'Create User' }}
              </h2>
              <p class="mt-1 text-sm text-gray-500">
                Enter the account information below.
              </p>
            </div>

            <button
              type="button"
              @click="closeModal"
              class="rounded-lg px-3 py-2 text-gray-400 hover:bg-white/5 hover:text-white"
              aria-label="Close dialog"
            >
              ✕
            </button>
          </header>

          <form @submit.prevent="saveUser" class="space-y-5 p-6">
            <div
              v-if="formError"
              role="alert"
              class="rounded-xl border border-red-500/30 bg-red-500/10 p-3 text-sm text-red-300"
            >
              {{ formError }}
            </div>

            <div class="grid grid-cols-1 gap-4 sm:grid-cols-2">
              <label class="block">
                <span class="mb-2 block text-sm text-gray-300">First name</span>
                <input
                  v-model="form.first_name"
                  type="text"
                  autocomplete="given-name"
                  class="w-full rounded-xl border border-white/10 bg-[#070A0F] px-4 py-3 text-sm outline-none focus:border-[#B7FF3C]/60"
                />
              </label>

              <label class="block">
                <span class="mb-2 block text-sm text-gray-300">Last name</span>
                <input
                  v-model="form.last_name"
                  type="text"
                  autocomplete="family-name"
                  class="w-full rounded-xl border border-white/10 bg-[#070A0F] px-4 py-3 text-sm outline-none focus:border-[#B7FF3C]/60"
                />
              </label>

              <label class="block">
                <span class="mb-2 block text-sm text-gray-300">Username *</span>
                <input
                  v-model="form.username"
                  type="text"
                  required
                  autocomplete="username"
                  class="w-full rounded-xl border border-white/10 bg-[#070A0F] px-4 py-3 text-sm outline-none focus:border-[#B7FF3C]/60"
                />
              </label>

              <label class="block">
                <span class="mb-2 block text-sm text-gray-300">Email *</span>
                <input
                  v-model="form.email"
                  type="email"
                  required
                  autocomplete="email"
                  class="w-full rounded-xl border border-white/10 bg-[#070A0F] px-4 py-3 text-sm outline-none focus:border-[#B7FF3C]/60"
                />
              </label>

              <label class="block">
                <span class="mb-2 block text-sm text-gray-300">Role</span>
                <select
                  v-model="form.role"
                  class="w-full rounded-xl border border-white/10 bg-[#070A0F] px-4 py-3 text-sm outline-none focus:border-[#B7FF3C]/60"
                >
                  <option value="user">User</option>
                  <option value="analyst">Analyst</option>
                  <option value="scout">Scout</option>
                  <option value="admin">Admin</option>
                </select>
              </label>

              <label class="block">
                <span class="mb-2 block text-sm text-gray-300">
                  Password {{ editingUserId === null ? '*' : '(optional)' }}
                </span>
                <input
                  v-model="form.password"
                  type="password"
                  :required="editingUserId === null"
                  :autocomplete="editingUserId === null ? 'new-password' : 'off'"
                  minlength="8"
                  :placeholder="editingUserId !== null ? 'Leave blank to keep current password' : 'At least 8 characters'"
                  class="w-full rounded-xl border border-white/10 bg-[#070A0F] px-4 py-3 text-sm outline-none focus:border-[#B7FF3C]/60"
                />
              </label>
            </div>

            <label class="flex cursor-pointer items-center justify-between rounded-xl border border-white/[0.07] bg-[#070A0F] p-4">
              <span>
                <span class="block text-sm font-medium">Account status</span>
                <span class="mt-1 block text-xs text-gray-500">
                  Allow or prevent this user from signing in.
                </span>
              </span>

              <input
                v-model="form.is_active"
                type="checkbox"
                class="h-5 w-5 accent-[#B7FF3C]"
              />
            </label>

            <footer class="flex justify-end gap-3 border-t border-white/[0.07] pt-5">
              <button
                type="button"
                @click="closeModal"
                :disabled="saving"
                class="rounded-xl border border-white/10 px-5 py-3 text-sm text-gray-300 hover:bg-white/5 disabled:opacity-50"
              >
                Cancel
              </button>

              <button
                type="submit"
                :disabled="saving"
                class="rounded-xl bg-[#B7FF3C] px-6 py-3 text-sm font-bold text-black transition hover:bg-[#caff65] disabled:cursor-not-allowed disabled:opacity-50"
              >
                {{ saving ? 'Saving...' : editingUserId !== null ? 'Save Changes' : 'Create User' }}
              </button>
            </footer>
          </form>
        </section>
      </div>
    </Teleport>
  </main>
</template>
