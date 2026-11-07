<script setup lang="ts">
import { computed, ref } from 'vue'

type SettingsTab = 'general' | 'matches' | 'notifications' | 'security' | 'ai'

const activeTab = ref<SettingsTab>('general')
const saved = ref(false)

const settings = ref({
  siteName: 'FIDS',
  siteDescription: 'Football Intelligence Decision System',
  timezone: 'Africa/Cairo',
  language: 'en',
  dateFormat: 'DD/MM/YYYY',
  maintenanceMode: false,

  defaultMatchView: 'all',
  refreshInterval: '60',
  showLiveScores: true,
  showMatchStatistics: true,
  showPredictions: true,

  emailNotifications: true,
  matchAlerts: true,
  scoutingAlerts: true,
  intelligenceAlerts: true,
  systemAlerts: false,

  twoFactorAuth: false,
  sessionTimeout: '30',
  loginNotifications: true,

  aiPredictions: true,
  aiScouting: true,
  aiNewsAnalysis: true,
  aiConfidenceThreshold: 75,
  aiProvider: 'default',
})

const tabs: { id: SettingsTab; label: string; icon: string; description: string }[] = [
  { id: 'general', label: 'General', icon: '⚙', description: 'Manage your platform preferences' },
  { id: 'matches', label: 'Matches', icon: '⚽', description: 'Configure match data and display' },
  { id: 'notifications', label: 'Notifications', icon: '♧', description: 'Control alerts and updates' },
  { id: 'security', label: 'Security', icon: '⬡', description: 'Protect your account and sessions' },
  { id: 'ai', label: 'AI Intelligence', icon: '✳', description: 'Configure AI-powered features' },
]

const currentTab = computed(() => tabs.find((tab) => tab.id === activeTab.value))

function saveSettings() {
  // Demo only: connect this function to your Django API to persist settings.
  saved.value = true
  setTimeout(() => {
    saved.value = false
  }, 3000)
}

function resetSettings() {
  settings.value = {
    siteName: 'FIDS',
    siteDescription: 'Football Intelligence Decision System',
    timezone: 'Africa/Cairo',
    language: 'en',
    dateFormat: 'DD/MM/YYYY',
    maintenanceMode: false,

    defaultMatchView: 'all',
    refreshInterval: '60',
    showLiveScores: true,
    showMatchStatistics: true,
    showPredictions: true,

    emailNotifications: true,
    matchAlerts: true,
    scoutingAlerts: true,
    intelligenceAlerts: true,
    systemAlerts: false,

    twoFactorAuth: false,
    sessionTimeout: '30',
    loginNotifications: true,

    aiPredictions: true,
    aiScouting: true,
    aiNewsAnalysis: true,
    aiConfidenceThreshold: 75,
    aiProvider: 'default',
  }
  saved.value = false
}
</script>

<template>
  <div class="min-h-screen bg-[#090d16] px-4 py-6 text-slate-100 sm:px-6 lg:px-8">
    <div class="mx-auto max-w-7xl space-y-7">
      <!-- Header -->
      <header class="flex flex-col justify-between gap-5 sm:flex-row sm:items-center">
        <div>
          <div class="mb-2 flex items-center gap-2 text-xs font-semibold uppercase tracking-[0.22em] text-cyan-400">
            <span class="h-2 w-2 rounded-full bg-cyan-400"></span>
            System administration
          </div>
          <h1 class="text-3xl font-bold tracking-tight text-white sm:text-4xl">
            Settings<span class="text-cyan-400">.</span>
          </h1>
          <p class="mt-2 text-sm text-slate-400">
            Manage your FIDS platform configuration and preferences.
          </p>
        </div>

        <div class="flex flex-wrap items-center gap-3">
          <button
            type="button"
            class="rounded-xl border border-slate-700 bg-slate-900 px-4 py-2.5 text-sm font-medium text-slate-300 transition hover:border-slate-500 hover:text-white"
            @click="resetSettings"
          >
            Reset defaults
          </button>
          <button
            type="button"
            class="inline-flex items-center gap-2 rounded-xl bg-cyan-400 px-5 py-2.5 text-sm font-bold text-slate-950 transition hover:bg-cyan-300"
            @click="saveSettings"
          >
            <span>✓</span>
            Save changes
          </button>
        </div>
      </header>

      <!-- Save feedback -->
      <div
        v-if="saved"
        class="flex items-center gap-3 rounded-xl border border-emerald-500/30 bg-emerald-500/10 px-4 py-3 text-sm text-emerald-300"
        role="status"
      >
        <span class="flex h-7 w-7 items-center justify-center rounded-full bg-emerald-500/15">✓</span>
        Settings updated in this page's current session. Connect the backend to save them permanently.
      </div>

      <!-- Status banner -->
      <section class="flex flex-col justify-between gap-4 rounded-2xl border border-slate-800 bg-gradient-to-r from-[#111c2c] to-[#11121e] p-5 sm:flex-row sm:items-center sm:p-6">
        <div class="flex items-center gap-4">
          <div class="flex h-12 w-12 items-center justify-center rounded-2xl border border-cyan-400/20 bg-cyan-400/10 text-xl text-cyan-300">
            ⚙
          </div>
          <div>
            <h2 class="font-semibold text-white">Platform configuration</h2>
            <p class="mt-1 text-sm text-slate-400">Customize how your football intelligence system operates.</p>
          </div>
        </div>
        <div class="flex items-center gap-2 self-start rounded-full border border-emerald-500/20 bg-emerald-500/10 px-3 py-1.5 sm:self-auto">
          <span class="h-2 w-2 rounded-full bg-emerald-400"></span>
          <span class="text-xs font-medium text-emerald-300">Dashboard available</span>
        </div>
      </section>

      <div class="grid grid-cols-1 items-start gap-6 lg:grid-cols-[250px_minmax(0,1fr)]">
        <!-- Sidebar navigation -->
        <aside class="rounded-2xl border border-slate-800 bg-[#0e1420] p-3">
          <p class="px-3 pb-3 pt-2 text-[10px] font-bold uppercase tracking-[0.2em] text-slate-500">
            Settings menu
          </p>

          <nav class="space-y-1" aria-label="Settings sections">
            <button
              v-for="tab in tabs"
              :key="tab.id"
              type="button"
              class="flex w-full items-start gap-3 rounded-xl px-3 py-3 text-left transition"
              :class="activeTab === tab.id
                ? 'border border-cyan-400/20 bg-cyan-400/10 text-cyan-300'
                : 'border border-transparent text-slate-400 hover:bg-slate-800/60 hover:text-white'"
              :aria-current="activeTab === tab.id ? 'page' : undefined"
              @click="activeTab = tab.id"
            >
              <span class="flex h-9 w-9 shrink-0 items-center justify-center rounded-lg bg-slate-800 text-base">
                {{ tab.icon }}
              </span>
              <span class="min-w-0 pt-0.5">
                <span class="block text-sm font-semibold">{{ tab.label }}</span>
                <span class="mt-1 block text-xs leading-5 text-slate-500">{{ tab.description }}</span>
              </span>
            </button>
          </nav>

          <div class="mt-4 rounded-xl border border-slate-800 bg-[#090d16] p-4">
            <div class="flex items-center gap-2 text-xs font-semibold text-slate-300">
              <span class="text-cyan-400">✳</span>
              FIDS Control Center
            </div>
            <p class="mt-2 text-xs leading-5 text-slate-500">
              Keep your platform preferences aligned with your workflow.
            </p>
          </div>
        </aside>

        <!-- Settings content -->
        <main class="min-w-0 rounded-2xl border border-slate-800 bg-[#0e1420]">
          <div class="border-b border-slate-800 px-5 py-5 sm:px-7">
            <div class="flex items-center gap-3">
              <span class="flex h-10 w-10 items-center justify-center rounded-xl bg-cyan-400/10 text-lg text-cyan-300">
                {{ currentTab?.icon }}
              </span>
              <div>
                <h2 class="text-lg font-bold text-white">{{ currentTab?.label }}</h2>
                <p class="mt-1 text-sm text-slate-400">{{ currentTab?.description }}</p>
              </div>
            </div>
          </div>

          <div class="space-y-7 p-5 sm:p-7">
            <!-- General -->
            <template v-if="activeTab === 'general'">
              <section>
                <h3 class="text-sm font-semibold text-white">Platform information</h3>
                <p class="mt-1 text-xs text-slate-500">Set the identity and basic preferences of your platform.</p>

                <div class="mt-5 grid grid-cols-1 gap-5 sm:grid-cols-2">
                  <label class="block">
                    <span class="mb-2 block text-sm text-slate-300">Platform name</span>
                    <input
                      v-model="settings.siteName"
                      type="text"
                      class="w-full rounded-xl border border-slate-700 bg-[#090d16] px-4 py-3 text-sm text-white outline-none transition focus:border-cyan-400"
                      placeholder="FIDS"
                    />
                  </label>

                  <label class="block">
                    <span class="mb-2 block text-sm text-slate-300">Default language</span>
                    <select
                      v-model="settings.language"
                      class="w-full rounded-xl border border-slate-700 bg-[#090d16] px-4 py-3 text-sm text-white outline-none focus:border-cyan-400"
                    >
                      <option value="en">English</option>
                      <option value="ar">العربية</option>
                    </select>
                  </label>

                  <label class="block sm:col-span-2">
                    <span class="mb-2 block text-sm text-slate-300">Platform description</span>
                    <textarea
                      v-model="settings.siteDescription"
                      rows="3"
                      class="w-full resize-y rounded-xl border border-slate-700 bg-[#090d16] px-4 py-3 text-sm text-white outline-none focus:border-cyan-400"
                      placeholder="Describe your platform..."
                    ></textarea>
                  </label>

                  <label class="block">
                    <span class="mb-2 block text-sm text-slate-300">Timezone</span>
                    <select
                      v-model="settings.timezone"
                      class="w-full rounded-xl border border-slate-700 bg-[#090d16] px-4 py-3 text-sm text-white outline-none focus:border-cyan-400"
                    >
                      <option value="Africa/Cairo">Africa / Cairo</option>
                      <option value="Europe/London">Europe / London</option>
                      <option value="Europe/Paris">Europe / Paris</option>
                      <option value="UTC">UTC</option>
                      <option value="America/New_York">America / New York</option>
                    </select>
                  </label>

                  <label class="block">
                    <span class="mb-2 block text-sm text-slate-300">Date format</span>
                    <select
                      v-model="settings.dateFormat"
                      class="w-full rounded-xl border border-slate-700 bg-[#090d16] px-4 py-3 text-sm text-white outline-none focus:border-cyan-400"
                    >
                      <option value="DD/MM/YYYY">DD/MM/YYYY</option>
                      <option value="MM/DD/YYYY">MM/DD/YYYY</option>
                      <option value="YYYY-MM-DD">YYYY-MM-DD</option>
                    </select>
                  </label>
                </div>
              </section>

              <div class="h-px bg-slate-800"></div>

              <section>
                <h3 class="text-sm font-semibold text-white">Maintenance mode</h3>
                <p class="mt-1 text-xs text-slate-500">Control whether the platform should be placed into maintenance mode.</p>

                <SettingToggle
                  v-model="settings.maintenanceMode"
                  title="Enable maintenance mode"
                  description="This is a local preference only; it does not restrict public access until implemented in the backend."
                  class="mt-4"
                />
              </section>
            </template>

            <!-- Matches -->
            <template v-else-if="activeTab === 'matches'">
              <section>
                <h3 class="text-sm font-semibold text-white">Match display</h3>
                <p class="mt-1 text-xs text-slate-500">Customize how match information is presented.</p>

                <div class="mt-5 grid grid-cols-1 gap-5 sm:grid-cols-2">
                  <label class="block">
                    <span class="mb-2 block text-sm text-slate-300">Default match view</span>
                    <select
                      v-model="settings.defaultMatchView"
                      class="w-full rounded-xl border border-slate-700 bg-[#090d16] px-4 py-3 text-sm text-white outline-none focus:border-cyan-400"
                    >
                      <option value="all">All matches</option>
                      <option value="live">Live matches</option>
                      <option value="upcoming">Upcoming matches</option>
                      <option value="finished">Finished matches</option>
                    </select>
                  </label>

                  <label class="block">
                    <span class="mb-2 block text-sm text-slate-300">Data refresh interval</span>
                    <select
                      v-model="settings.refreshInterval"
                      class="w-full rounded-xl border border-slate-700 bg-[#090d16] px-4 py-3 text-sm text-white outline-none focus:border-cyan-400"
                    >
                      <option value="15">Every 15 seconds</option>
                      <option value="30">Every 30 seconds</option>
                      <option value="60">Every 60 seconds</option>
                      <option value="300">Every 5 minutes</option>
                    </select>
                  </label>
                </div>
              </section>

              <div class="h-px bg-slate-800"></div>

              <section>
                <h3 class="text-sm font-semibold text-white">Match features</h3>
                <div class="mt-4 space-y-3">
                  <SettingToggle
                    v-model="settings.showLiveScores"
                    title="Live scores"
                    description="Display live scores in match listings."
                  />
                  <SettingToggle
                    v-model="settings.showMatchStatistics"
                    title="Match statistics"
                    description="Show possession, shots, and other available statistics."
                  />
                  <SettingToggle
                    v-model="settings.showPredictions"
                    title="AI match predictions"
                    description="Display predictions when supported by the backend."
                  />
                </div>
              </section>
            </template>

            <!-- Notifications -->
            <template v-else-if="activeTab === 'notifications'">
              <section>
                <h3 class="text-sm font-semibold text-white">Notification preferences</h3>
                <p class="mt-1 text-xs text-slate-500">Choose the types of alerts you want to receive.</p>

                <div class="mt-5 space-y-3">
                  <SettingToggle
                    v-model="settings.emailNotifications"
                    title="Email notifications"
                    description="Enable email notifications globally."
                  />
                  <SettingToggle
                    v-model="settings.matchAlerts"
                    title="Match alerts"
                    description="Alerts about match events and score changes."
                  />
                  <SettingToggle
                    v-model="settings.scoutingAlerts"
                    title="Scouting alerts"
                    description="Updates about prospects and scouting recommendations."
                  />
                  <SettingToggle
                    v-model="settings.intelligenceAlerts"
                    title="Intelligence reports"
                    description="Notifications about generated insights and analysis."
                  />
                  <SettingToggle
                    v-model="settings.systemAlerts"
                    title="System alerts"
                    description="Receive platform health and administrative alerts."
                  />
                </div>
              </section>

              <div class="rounded-xl border border-amber-400/20 bg-amber-400/5 p-4">
                <p class="text-sm font-medium text-amber-300">Notification delivery</p>
                <p class="mt-1 text-xs leading-5 text-slate-400">
                  These switches update the interface only. Email delivery requires a configured backend notification service.
                </p>
              </div>
            </template>

            <!-- Security -->
            <template v-else-if="activeTab === 'security'">
              <section>
                <h3 class="text-sm font-semibold text-white">Account protection</h3>
                <p class="mt-1 text-xs text-slate-500">Review security preferences for your administrator account.</p>

                <div class="mt-5 space-y-3">
                  <SettingToggle
                    v-model="settings.twoFactorAuth"
                    title="Two-factor authentication"
                    description="Preference toggle only. Actual two-factor authentication must be implemented server-side."
                  />
                  <SettingToggle
                    v-model="settings.loginNotifications"
                    title="Login notifications"
                    description="Enable alerts about account sign-in activity when supported."
                  />
                </div>
              </section>

              <div class="h-px bg-slate-800"></div>

              <section>
                <h3 class="text-sm font-semibold text-white">Session management</h3>
                <p class="mt-1 text-xs text-slate-500">Choose a preferred session timeout.</p>

                <label class="mt-5 block max-w-sm">
                  <span class="mb-2 block text-sm text-slate-300">Session timeout</span>
                  <select
                    v-model="settings.sessionTimeout"
                    class="w-full rounded-xl border border-slate-700 bg-[#090d16] px-4 py-3 text-sm text-white outline-none focus:border-cyan-400"
                  >
                    <option value="15">15 minutes</option>
                    <option value="30">30 minutes</option>
                    <option value="60">1 hour</option>
                    <option value="120">2 hours</option>
                  </select>
                </label>

                <div class="mt-5 rounded-xl border border-slate-800 bg-[#090d16] p-4">
                  <div class="flex items-start gap-3">
                    <span class="text-lg text-cyan-400">ⓘ</span>
                    <div>
                      <p class="text-sm font-medium text-slate-200">Security implementation required</p>
                      <p class="mt-1 text-xs leading-5 text-slate-500">
                        Changing these values does not modify Django authentication, JWT expiry, or server sessions.
                        Enforce security settings through your backend before relying on them.
                      </p>
                    </div>
                  </div>
                </div>
              </section>
            </template>

            <!-- AI Intelligence -->
            <template v-else-if="activeTab === 'ai'">
              <section>
                <h3 class="text-sm font-semibold text-white">AI features</h3>
                <p class="mt-1 text-xs text-slate-500">Choose which AI capabilities should be enabled in your platform.</p>

                <div class="mt-5 space-y-3">
                  <SettingToggle
                    v-model="settings.aiPredictions"
                    title="Match predictions"
                    description="Enable AI-assisted match prediction features."
                  />
                  <SettingToggle
                    v-model="settings.aiScouting"
                    title="Player scouting intelligence"
                    description="Enable prospect analysis and scouting recommendations."
                  />
                  <SettingToggle
                    v-model="settings.aiNewsAnalysis"
                    title="News analysis"
                    description="Enable AI-assisted analysis of football news."
                  />
                </div>
              </section>

              <div class="h-px bg-slate-800"></div>

              <section>
                <h3 class="text-sm font-semibold text-white">Analysis configuration</h3>

                <label class="mt-5 block">
                  <span class="flex items-center justify-between gap-4 text-sm text-slate-300">
                    <span>Minimum confidence threshold</span>
                    <span class="font-semibold text-cyan-300">{{ settings.aiConfidenceThreshold }}%</span>
                  </span>
                  <input
                    v-model.number="settings.aiConfidenceThreshold"
                    type="range"
                    min="50"
                    max="95"
                    step="5"
                    class="mt-4 w-full cursor-pointer accent-cyan-400"
                  />
                  <span class="mt-2 flex justify-between text-xs text-slate-500">
                    <span>50% — Lower</span>
                    <span>95% — Higher</span>
                  </span>
                </label>

                <label class="mt-5 block max-w-sm">
                  <span class="mb-2 block text-sm text-slate-300">AI provider</span>
                  <select
                    v-model="settings.aiProvider"
                    class="w-full rounded-xl border border-slate-700 bg-[#090d16] px-4 py-3 text-sm text-white outline-none focus:border-cyan-400"
                  >
                    <option value="default">Default provider</option>
                    <option value="openai">OpenAI (configure backend first)</option>
                    <option value="local">Local model (configure backend first)</option>
                  </select>
                </label>
              </section>

              <div class="rounded-xl border border-violet-400/20 bg-violet-400/5 p-4">
                <p class="text-sm font-medium text-violet-300">AI configuration note</p>
                <p class="mt-1 text-xs leading-5 text-slate-400">
                  Do not expose API keys in this frontend. Configure provider credentials and model selection securely in Django environment variables or backend settings.
                </p>
              </div>
            </template>

            <!-- Bottom actions -->
            <div class="flex flex-col justify-between gap-4 border-t border-slate-800 pt-6 sm:flex-row sm:items-center">
              <p class="text-xs text-slate-500">
                Changes are currently held in frontend memory.
              </p>
              <button
                type="button"
                class="inline-flex items-center justify-center gap-2 rounded-xl bg-cyan-400 px-5 py-3 text-sm font-bold text-slate-950 transition hover:bg-cyan-300"
                @click="saveSettings"
              >
                ✓ Save {{ currentTab?.label }} settings
              </button>
            </div>
          </div>
        </main>
      </div>

      <footer class="flex flex-col justify-between gap-2 border-t border-slate-800 pt-5 text-xs text-slate-500 sm:flex-row">
        <span>FIDS · Football Intelligence Decision System</span>
        <span>Admin Settings · Demo configuration</span>
      </footer>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue'

export default defineComponent({
  components: {
    SettingToggle: defineComponent({
      name: 'SettingToggle',
      props: {
        modelValue: { type: Boolean, required: true },
        title: { type: String, required: true },
        description: { type: String, required: true },
      },
      emits: ['update:modelValue'],
      template: `
        <div class="flex items-center justify-between gap-4 rounded-xl border border-slate-800 bg-[#090d16] p-4">
          <div class="min-w-0">
            <p class="text-sm font-medium text-slate-200">{{ title }}</p>
            <p class="mt-1 text-xs leading-5 text-slate-500">{{ description }}</p>
          </div>
          <button
            type="button"
            role="switch"
            :aria-checked="modelValue"
            :aria-label="title"
            @click="$emit('update:modelValue', !modelValue)"
            class="relative inline-flex h-6 w-11 shrink-0 items-center rounded-full transition-colors focus:outline-none focus:ring-2 focus:ring-cyan-400/50"
            :class="modelValue ? 'bg-cyan-400' : 'bg-slate-700'"
          >
            <span
              class="inline-block h-4 w-4 transform rounded-full bg-white shadow transition-transform"
              :class="modelValue ? 'translate-x-6' : 'translate-x-1'"
            ></span>
          </button>
        </div>
      `,
    }),
  },
})
</script>
