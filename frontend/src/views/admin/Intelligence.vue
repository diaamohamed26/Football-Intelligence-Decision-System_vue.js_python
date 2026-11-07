<template>
  <div class="min-h-screen bg-slate-950 p-4 text-slate-100 sm:p-6 lg:p-8">
    <!-- Header -->
    <header
      class="mb-8 flex flex-col gap-5 sm:flex-row sm:items-center sm:justify-between"
    >
      <div>
        <p
          class="mb-2 text-xs font-bold uppercase tracking-[0.2em] text-indigo-400"
        >
          Administration / AI Systems
        </p>

        <h1 class="text-3xl font-bold tracking-tight sm:text-4xl">
          Intelligence Center
        </h1>

        <p class="mt-3 text-sm text-slate-400">
          Monitor AI-powered football analysis and system performance.
        </p>
      </div>

      <span
        class="inline-flex w-fit items-center gap-2 rounded-full border border-emerald-500/20 bg-emerald-500/10 px-4 py-2 text-xs font-medium text-emerald-400"
      >
        <span class="h-2 w-2 rounded-full bg-emerald-400"></span>
        System Operational
      </span>
    </header>

    <!-- Statistics -->
    <section
      class="mb-6 grid grid-cols-1 gap-4 sm:grid-cols-2 xl:grid-cols-4"
    >
      <article
        v-for="stat in statCards"
        :key="stat.label"
        class="rounded-2xl border border-slate-800 bg-slate-900 p-5 transition hover:border-slate-700"
      >
        <div
          class="mb-5 flex h-11 w-11 items-center justify-center rounded-xl text-xl"
          :class="stat.iconClass"
        >
          {{ stat.icon }}
        </div>

        <p class="text-sm text-slate-400">
          {{ stat.label }}
        </p>

        <h2 class="mt-2 text-3xl font-bold tracking-tight">
          {{ stat.value }}
        </h2>

        <p class="mt-3 text-xs text-slate-500">
          {{ stat.description }}
        </p>
      </article>
    </section>

    <!-- Services and Overview -->
    <section class="mb-6 grid grid-cols-1 gap-6 xl:grid-cols-2">
      <!-- AI Services -->
      <article
        class="rounded-2xl border border-slate-800 bg-slate-900 p-5 sm:p-6"
      >
        <div class="mb-6 flex items-center justify-between gap-3">
          <div>
            <h2 class="text-lg font-semibold">AI Services</h2>
            <p class="mt-1 text-sm text-slate-400">
              Current service availability
            </p>
          </div>

          <span
            class="rounded-lg bg-indigo-500/10 px-3 py-2 text-[10px] font-bold tracking-wider text-indigo-400"
          >
            LIVE STATUS
          </span>
        </div>

        <div
          v-for="service in services"
          :key="service.name"
          class="flex items-center justify-between gap-3 border-b border-slate-800 py-5 last:border-0 last:pb-0"
        >
          <div class="flex min-w-0 items-center gap-3">
            <div
              class="flex h-11 w-11 shrink-0 items-center justify-center rounded-xl bg-slate-800 text-xl"
              :class="service.iconClass"
            >
              {{ service.icon }}
            </div>

            <div class="min-w-0">
              <h3 class="text-sm font-medium text-slate-100">
                {{ service.name }}
              </h3>

              <p class="mt-1 text-xs leading-5 text-slate-400">
                {{ service.description }}
              </p>
            </div>
          </div>

          <span
            class="inline-flex shrink-0 items-center gap-2 rounded-full px-3 py-2 text-xs font-medium"
            :class="statusClasses(service.status)"
          >
            <span
              class="h-1.5 w-1.5 rounded-full"
              :class="statusDotClasses(service.status)"
            ></span>
            {{ service.status }}
          </span>
        </div>
      </article>

      <!-- Intelligence Overview -->
      <article
        class="rounded-2xl border border-slate-800 bg-slate-900 p-5 sm:p-6"
      >
        <div class="mb-6">
          <h2 class="text-lg font-semibold">Intelligence Overview</h2>
          <p class="mt-1 text-sm text-slate-400">
            Current system configuration
          </p>
        </div>

        <div
          v-for="item in overview"
          :key="item.label"
          class="flex items-center justify-between gap-4 border-b border-slate-800 py-4 last:border-0"
        >
          <span class="text-sm text-slate-400">
            {{ item.label }}
          </span>

          <span
            class="text-right text-sm font-medium"
            :class="
              item.enabled === true
                ? 'text-emerald-400'
                : 'text-slate-200'
            "
          >
            {{ item.value }}
          </span>
        </div>

        <div
          class="mt-5 rounded-xl border border-indigo-500/20 bg-indigo-500/10 p-4"
        >
          <p class="text-xs leading-6 text-indigo-200">
            Demo statistics are currently displayed. Connect the Django API
            to load live intelligence data.
          </p>
        </div>
      </article>
    </section>

    <!-- Recent Activity -->
    <section
      class="overflow-hidden rounded-2xl border border-slate-800 bg-slate-900"
    >
      <div class="border-b border-slate-800 p-5 sm:p-6">
        <h2 class="text-lg font-semibold">Recent AI Activity</h2>
        <p class="mt-1 text-sm text-slate-400">
          Latest recorded intelligence operations
        </p>
      </div>

      <div class="overflow-x-auto">
        <table class="w-full min-w-[650px] text-left">
          <thead class="bg-slate-950/50">
            <tr>
              <th
                class="px-6 py-4 text-xs font-semibold uppercase tracking-wider text-slate-400"
              >
                Operation
              </th>
              <th
                class="px-6 py-4 text-xs font-semibold uppercase tracking-wider text-slate-400"
              >
                Module
              </th>
              <th
                class="px-6 py-4 text-xs font-semibold uppercase tracking-wider text-slate-400"
              >
                Status
              </th>
              <th
                class="px-6 py-4 text-xs font-semibold uppercase tracking-wider text-slate-400"
              >
                Response Time
              </th>
            </tr>
          </thead>

          <tbody>
            <tr
              v-for="activity in activities"
              :key="activity.id"
              class="border-t border-slate-800 transition hover:bg-slate-800/40"
            >
              <td class="px-6 py-5 text-sm font-medium text-slate-200">
                {{ activity.operation }}
              </td>

              <td class="px-6 py-5 text-sm text-slate-400">
                {{ activity.module }}
              </td>

              <td class="px-6 py-5">
                <span
                  class="inline-flex items-center gap-2 rounded-full px-3 py-1.5 text-xs font-medium"
                  :class="statusClasses(activity.status)"
                >
                  <span
                    class="h-1.5 w-1.5 rounded-full"
                    :class="statusDotClasses(activity.status)"
                  ></span>
                  {{ activity.status }}
                </span>
              </td>

              <td class="px-6 py-5 text-sm text-slate-300">
                {{ activity.responseTime }} ms
              </td>
            </tr>

            <tr v-if="activities.length === 0">
              <td colspan="4" class="px-6 py-12 text-center text-sm text-slate-500">
                No AI activity recorded yet.
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue'

type ServiceStatus = 'Online' | 'Offline' | 'Maintenance'
type ActivityStatus = 'Success' | 'Failed' | 'Processing'

interface Service {
  name: string
  description: string
  icon: string
  iconClass: string
  status: ServiceStatus
}

interface Activity {
  id: number
  operation: string
  module: string
  status: ActivityStatus
  responseTime: number
}

const stats = ref({
  totalRequests: 12840,
  responseTime: 245,
  successRate: 98.6,
  activeModels: 3,
})

const statCards = computed(() => [
  {
    label: 'Total AI Requests',
    value: stats.value.totalRequests.toLocaleString(),
    description: 'All-time requests',
    icon: '✦',
    iconClass: 'bg-violet-500/10 text-violet-400',
  },
  {
    label: 'Average Response',
    value: `${stats.value.responseTime} ms`,
    description: 'Average processing time',
    icon: '◷',
    iconClass: 'bg-blue-500/10 text-blue-400',
  },
  {
    label: 'Success Rate',
    value: `${stats.value.successRate}%`,
    description: 'Successful AI operations',
    icon: '✓',
    iconClass: 'bg-emerald-500/10 text-emerald-400',
  },
  {
    label: 'Active Models',
    value: String(stats.value.activeModels),
    description: 'Configured AI models',
    icon: '◎',
    iconClass: 'bg-orange-500/10 text-orange-400',
  },
])

const services = ref<Service[]>([
  {
    name: 'Match Analysis',
    description: 'Match statistics and performance insights',
    icon: '⚽',
    iconClass: 'text-emerald-400',
    status: 'Online',
  },
  {
    name: 'Prediction Engine',
    description: 'Football match prediction processing',
    icon: '✦',
    iconClass: 'text-violet-400',
    status: 'Online',
  },
  {
    name: 'Player Scouting',
    description: 'Player evaluation and talent discovery',
    icon: '◎',
    iconClass: 'text-blue-400',
    status: 'Online',
  },
  {
    name: 'AI Assistant',
    description: 'Natural language football assistance',
    icon: '◈',
    iconClass: 'text-orange-400',
    status: 'Online',
  },
])

const overview = ref([
  { label: 'Prediction Engine', value: 'Football Analytics', enabled: false },
  { label: 'Data Processing', value: 'Enabled', enabled: true },
  { label: 'Match Analysis', value: 'Enabled', enabled: true },
  { label: 'Scouting Insights', value: 'Enabled', enabled: true },
  { label: 'Environment', value: 'Development', enabled: false },
])

const activities = ref<Activity[]>([
  {
    id: 1,
    operation: 'Match performance analysis',
    module: 'Match Analysis',
    status: 'Success',
    responseTime: 218,
  },
  {
    id: 2,
    operation: 'Player evaluation',
    module: 'Scouting',
    status: 'Success',
    responseTime: 305,
  },
  {
    id: 3,
    operation: 'Match prediction',
    module: 'Prediction Engine',
    status: 'Success',
    responseTime: 192,
  },
  {
    id: 4,
    operation: 'Football question processing',
    module: 'AI Assistant',
    status: 'Success',
    responseTime: 264,
  },
])

function statusClasses(status: string): string {
  switch (status) {
    case 'Online':
    case 'Success':
      return 'bg-emerald-500/10 text-emerald-400'

    case 'Offline':
    case 'Failed':
      return 'bg-red-500/10 text-red-400'

    case 'Maintenance':
    case 'Processing':
      return 'bg-amber-500/10 text-amber-400'

    default:
      return 'bg-slate-800 text-slate-300'
  }
}

function statusDotClasses(status: string): string {
  switch (status) {
    case 'Online':
    case 'Success':
      return 'bg-emerald-400'

    case 'Offline':
    case 'Failed':
      return 'bg-red-400'

    case 'Maintenance':
    case 'Processing':
      return 'bg-amber-400'

    default:
      return 'bg-slate-400'
  }
}
</script>
