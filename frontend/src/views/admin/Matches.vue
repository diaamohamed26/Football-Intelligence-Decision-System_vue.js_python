
<template>
  <div class="min-h-screen space-y-7 bg-[#070A0F] p-4 text-slate-100 sm:p-6 lg:p-8">

    <!-- Header -->
    <header class="flex flex-col justify-between gap-5 lg:flex-row lg:items-center">
      <div>
        <div class="mb-3 flex items-center gap-2 text-xs font-semibold uppercase tracking-[0.2em] text-indigo-400">
          <span>FIDS</span>
          <span class="text-slate-700">/</span>
          <span>Administration</span>
          <span class="text-slate-700">/</span>
          <span class="text-slate-400">Matches</span>
        </div>

        <h1 class="text-3xl font-bold tracking-tight sm:text-4xl">
          Match Management
        </h1>

        <p class="mt-2 text-sm text-slate-400">
          Manage fixtures, live scores, results and competition schedules.
        </p>
      </div>

      <div class="flex flex-wrap items-center gap-3">
        <button
          type="button"
          :disabled="loading"
          class="flex items-center gap-2 rounded-xl border border-slate-800 bg-[#0F141C] px-4 py-3 text-sm font-medium text-slate-300 transition hover:border-slate-600 hover:text-white disabled:opacity-50"
          @click="loadData"
        >
          <span :class="{ 'animate-spin': loading }">↻</span>
          Refresh
        </button>

        <button
          type="button"
          class="flex items-center gap-2 rounded-xl bg-indigo-600 px-5 py-3 text-sm font-semibold text-white shadow-lg shadow-indigo-950/30 transition hover:bg-indigo-500"
          @click="openCreateModal"
        >
          <span class="text-lg">+</span>
          Add New Match
        </button>
      </div>
    </header>

    <!-- Notifications -->
    <div
      v-if="pageError"
      class="flex items-start gap-3 rounded-xl border border-red-500/20 bg-red-500/10 p-4 text-sm text-red-300"
    >
      <span class="text-lg">!</span>
      <div class="flex-1">{{ pageError }}</div>
      <button
        type="button"
        class="text-red-300 hover:text-white"
        @click="pageError = ''"
      >
        ×
      </button>
    </div>

    <div
      v-if="notice"
      class="flex items-center justify-between rounded-xl border border-emerald-500/20 bg-emerald-500/10 p-4 text-sm text-emerald-300"
    >
      <span>✓ {{ notice }}</span>
      <button type="button" @click="notice = ''">×</button>
    </div>

    <!-- Statistics -->
    <section class="grid grid-cols-1 gap-4 sm:grid-cols-2 xl:grid-cols-4">
      <article
        v-for="stat in statCards"
        :key="stat.label"
        class="group relative overflow-hidden rounded-2xl border border-slate-800/80 bg-[#0F141C] p-5 transition hover:border-slate-700"
      >
        <div class="flex items-start justify-between">
          <div>
            <p class="text-sm font-medium text-slate-400">
              {{ stat.label }}
            </p>

            <h2 class="mt-3 text-3xl font-bold tracking-tight">
              {{ stat.value }}
            </h2>
          </div>

          <div
            class="flex h-12 w-12 items-center justify-center rounded-xl text-xl"
            :class="stat.iconClass"
          >
            {{ stat.icon }}
          </div>
        </div>

        <p class="mt-4 text-xs text-slate-500">
          {{ stat.description }}
        </p>
      </article>
    </section>

    <!-- Main Content -->
    <section class="overflow-hidden rounded-2xl border border-slate-800 bg-[#0F141C]">

      <!-- Section Heading -->
      <div class="flex flex-col justify-between gap-4 border-b border-slate-800 p-5 lg:flex-row lg:items-center">
        <div>
          <h2 class="text-lg font-semibold">All Matches</h2>
          <p class="mt-1 text-xs text-slate-500">
            View and manage all football fixtures.
          </p>
        </div>

        <div class="flex flex-wrap items-center gap-3">
          <div class="rounded-lg border border-slate-800 bg-[#070A0F] px-3 py-2 text-xs text-slate-400">
            <span class="font-semibold text-white">{{ filteredMatches.length }}</span>
            Matches found
          </div>

          <div class="rounded-lg border border-slate-800 bg-[#070A0F] px-3 py-2 text-xs text-slate-400">
            <span class="font-semibold text-white">{{ teams.length }}</span>
            Teams
          </div>

          <div class="rounded-lg border border-slate-800 bg-[#070A0F] px-3 py-2 text-xs text-slate-400">
            <span class="font-semibold text-white">{{ competitions.length }}</span>
            Competitions
          </div>
        </div>
      </div>

      <!-- Filters -->
      <div class="space-y-5 border-b border-slate-800 p-5">

        <!-- Status Tabs -->
        <div class="flex gap-2 overflow-x-auto pb-1">
          <button
            v-for="tab in statusTabs"
            :key="tab.value"
            type="button"
            class="flex shrink-0 items-center gap-2 rounded-lg border px-4 py-2.5 text-xs font-semibold transition"
            :class="
              selectedStatus === tab.value
                ? 'border-indigo-500/40 bg-indigo-500/10 text-indigo-300'
                : 'border-slate-800 bg-[#070A0F] text-slate-400 hover:border-slate-700 hover:text-white'
            "
            @click="selectedStatus = tab.value"
          >
            {{ tab.label }}

            <span
              class="rounded-md px-1.5 py-0.5 text-[10px]"
              :class="selectedStatus === tab.value ? 'bg-indigo-500/20' : 'bg-slate-800'"
            >
              {{ tab.count }}
            </span>
          </button>
        </div>

        <!-- Search and Filters -->
        <div class="grid grid-cols-1 gap-3 md:grid-cols-2 xl:grid-cols-4">

          <div class="relative">
            <span class="absolute left-4 top-1/2 -translate-y-1/2 text-slate-500">
              ⌕
            </span>

            <input
              v-model="searchQuery"
              type="search"
              placeholder="Search matches..."
              class="w-full rounded-xl border border-slate-800 bg-[#070A0F] py-3 pl-11 pr-4 text-sm outline-none transition placeholder:text-slate-600 focus:border-indigo-500"
            />
          </div>

          <select
            v-model="selectedCompetition"
            class="rounded-xl border border-slate-800 bg-[#070A0F] px-4 py-3 text-sm text-slate-300 outline-none focus:border-indigo-500"
          >
            <option value="All">All competitions</option>
            <option
              v-for="competition in competitions"
              :key="competition.id"
              :value="String(competition.id)"
            >
              {{ competition.name }}
            </option>
          </select>

          <input
            v-model="selectedDate"
            type="date"
            aria-label="Filter by date"
            class="rounded-xl border border-slate-800 bg-[#070A0F] px-4 py-3 text-sm text-slate-300 outline-none focus:border-indigo-500"
          />

          <button
            type="button"
            class="rounded-xl border border-slate-800 bg-[#070A0F] px-4 py-3 text-sm text-slate-400 transition hover:border-slate-600 hover:text-white"
            @click="resetFilters"
          >
            Reset all filters
          </button>
        </div>
      </div>

      <!-- Loading -->
      <div v-if="loading" class="flex flex-col items-center justify-center gap-4 p-20">
        <div class="h-9 w-9 animate-spin rounded-full border-2 border-slate-700 border-t-indigo-500"></div>
        <p class="text-sm text-slate-400">Loading match data...</p>
      </div>

      <!-- Matches Table -->
      <div v-else class="overflow-x-auto">
        <table class="w-full min-w-[1000px] text-left">

          <thead class="bg-[#070A0F]/70">
            <tr>
              <th class="px-6 py-4 text-[11px] font-semibold uppercase tracking-wider text-slate-500">
                Match
              </th>

              <th class="px-6 py-4 text-[11px] font-semibold uppercase tracking-wider text-slate-500">
                Competition
              </th>

              <th class="px-6 py-4 text-[11px] font-semibold uppercase tracking-wider text-slate-500">
                Date & Time
              </th>

              <th class="px-6 py-4 text-[11px] font-semibold uppercase tracking-wider text-slate-500">
                Score
              </th>

              <th class="px-6 py-4 text-[11px] font-semibold uppercase tracking-wider text-slate-500">
                Status
              </th>

              <th class="px-6 py-4 text-right text-[11px] font-semibold uppercase tracking-wider text-slate-500">
                Actions
              </th>
            </tr>
          </thead>

          <tbody>
            <tr
              v-for="match in filteredMatches"
              :key="match.id"
              class="border-t border-slate-800/80 transition hover:bg-white/[0.02]"
            >

              <!-- Teams -->
              <td class="px-6 py-5">
                <div class="flex min-w-[230px] items-center gap-4">

                  <div class="flex flex-col gap-2">
                    <div class="flex h-9 w-9 items-center justify-center rounded-lg bg-slate-800 text-[10px] font-bold text-indigo-300">
                      {{ initials(match.home_team_name) }}
                    </div>

                    <div class="flex h-9 w-9 items-center justify-center rounded-lg bg-slate-800 text-[10px] font-bold text-emerald-300">
                      {{ initials(match.away_team_name) }}
                    </div>
                  </div>

                  <div class="space-y-3">
                    <p class="text-sm font-semibold text-white">
                      {{ match.home_team_name }}
                    </p>

                    <p class="text-sm font-semibold text-slate-300">
                      {{ match.away_team_name }}
                    </p>
                  </div>
                </div>
              </td>

              <!-- Competition -->
              <td class="px-6 py-5">
                <p class="text-sm font-medium text-slate-200">
                  {{ match.competition_name || 'Friendly Match' }}
                </p>

                <p class="mt-1 text-xs text-slate-500">
                  {{ competitionSeason(match.competition) }}
                </p>
              </td>

              <!-- Date -->
              <td class="px-6 py-5">
                <p class="text-sm text-slate-200">
                  {{ formatDate(match.kickoff) }}
                </p>

                <p class="mt-1 text-xs text-slate-500">
                  {{ formatTime(match.kickoff) }}
                </p>
              </td>

              <!-- Score -->
              <td class="px-6 py-5">
                <div class="inline-flex items-center gap-3 rounded-lg border border-slate-800 bg-[#070A0F] px-4 py-2">
                  <span class="text-lg font-bold text-white">
                    {{ displayScore(match.home_score) }}
                  </span>

                  <span class="text-slate-600">:</span>

                  <span class="text-lg font-bold text-white">
                    {{ displayScore(match.away_score) }}
                  </span>
                </div>
              </td>

              <!-- Status -->
              <td class="px-6 py-5">
                <span
                  class="inline-flex items-center gap-2 rounded-full px-3 py-1.5 text-xs font-semibold"
                  :class="statusClasses(match.status)"
                >
                  <span
                    class="h-1.5 w-1.5 rounded-full"
                    :class="statusDotClasses(match.status)"
                  ></span>

                  {{ statusLabel(match.status) }}
                </span>
              </td>

              <!-- Actions -->
              <td class="px-6 py-5">
                <div class="flex justify-end gap-2">

                  <button
                    type="button"
                    class="rounded-lg border border-slate-700 px-3 py-2 text-xs text-slate-300 transition hover:border-indigo-500 hover:text-indigo-300"
                    @click="viewMatch(match)"
                  >
                    View
                  </button>

                  <button
                    type="button"
                    class="rounded-lg border border-slate-700 px-3 py-2 text-xs text-slate-300 transition hover:border-indigo-500 hover:text-indigo-300"
                    @click="openEditModal(match)"
                  >
                    Edit
                  </button>

                  <button
                    type="button"
                    :disabled="deletingId === match.id"
                    class="rounded-lg border border-red-500/20 px-3 py-2 text-xs text-red-400 transition hover:bg-red-500/10 disabled:opacity-50"
                    @click="deleteMatch(match)"
                  >
                    {{ deletingId === match.id ? 'Deleting...' : 'Delete' }}
                  </button>

                </div>
              </td>
            </tr>

            <!-- Empty State -->
            <tr v-if="filteredMatches.length === 0">
              <td colspan="6" class="px-6 py-20 text-center">

                <div class="mx-auto mb-4 flex h-16 w-16 items-center justify-center rounded-2xl border border-slate-800 bg-[#070A0F] text-3xl">
                  ⚽
                </div>

                <h3 class="font-semibold text-slate-200">
                  No matches found
                </h3>

                <p class="mt-2 text-sm text-slate-500">
                  There are no matches matching your current filters.
                </p>

                <button
                  type="button"
                  class="mt-5 text-sm font-semibold text-indigo-400 hover:text-indigo-300"
                  @click="resetFilters"
                >
                  Clear filters
                </button>

              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Footer -->
      <div class="flex flex-col justify-between gap-2 border-t border-slate-800 px-6 py-4 sm:flex-row sm:items-center">
        <p class="text-xs text-slate-500">
          Showing {{ filteredMatches.length }} of {{ matches.length }} matches
        </p>

        <p class="text-xs text-slate-600">
          FIDS Match Management
        </p>
      </div>
    </section>

    <!-- CREATE / EDIT MODAL -->
    <div
      v-if="showModal"
      class="fixed inset-0 z-50 flex items-center justify-center overflow-y-auto bg-black/80 p-4 backdrop-blur-sm"
      @click.self="closeModal"
    >
      <section class="my-auto w-full max-w-2xl overflow-hidden rounded-2xl border border-slate-700 bg-[#0F141C] shadow-2xl">

        <!-- Modal Header -->
        <div class="flex items-center justify-between border-b border-slate-800 p-6">
          <div>
            <div class="mb-2 text-xs font-semibold uppercase tracking-widest text-indigo-400">
              Match Management
            </div>

            <h2 class="text-xl font-bold">
              {{ editingId === null ? 'Create New Match' : 'Edit Match' }}
            </h2>

            <p class="mt-1 text-sm text-slate-500">
              Configure the match information below.
            </p>
          </div>

          <button
            type="button"
            aria-label="Close modal"
            class="flex h-9 w-9 items-center justify-center rounded-lg bg-slate-800 text-xl text-slate-400 transition hover:bg-slate-700 hover:text-white"
            @click="closeModal"
          >
            ×
          </button>
        </div>

        <!-- Modal Form -->
        <form class="space-y-6 p-6" @submit.prevent="saveMatch">

          <!-- Teams -->
          <div>
            <h3 class="mb-4 text-sm font-semibold text-slate-200">
              Teams
            </h3>

            <div class="grid grid-cols-1 gap-4 sm:grid-cols-2">

              <div>
                <label for="home-team" class="mb-2 block text-xs font-medium text-slate-400">
                  Home Team
                </label>

                <select
                  id="home-team"
                  v-model.number="form.home_team"
                  required
                  :disabled="teams.length === 0"
                  class="w-full rounded-xl border border-slate-700 bg-[#070A0F] px-4 py-3 text-sm text-white outline-none focus:border-indigo-500 disabled:opacity-50"
                >
                  <option :value="0" disabled>
                    {{ teams.length ? 'Select home team' : 'No teams available' }}
                  </option>

                  <option
                    v-for="team in teams"
                    :key="team.id"
                    :value="Number(team.id)"
                    :disabled="Number(team.id) === form.away_team"
                  >
                    {{ team.name }}
                  </option>
                </select>
              </div>

              <div>
                <label for="away-team" class="mb-2 block text-xs font-medium text-slate-400">
                  Away Team
                </label>

                <select
                  id="away-team"
                  v-model.number="form.away_team"
                  required
                  :disabled="teams.length === 0"
                  class="w-full rounded-xl border border-slate-700 bg-[#070A0F] px-4 py-3 text-sm text-white outline-none focus:border-indigo-500 disabled:opacity-50"
                >
                  <option :value="0" disabled>
                    {{ teams.length ? 'Select away team' : 'No teams available' }}
                  </option>

                  <option
                    v-for="team in teams"
                    :key="team.id"
                    :value="Number(team.id)"
                    :disabled="Number(team.id) === form.home_team"
                  >
                    {{ team.name }}
                  </option>
                </select>
              </div>
            </div>

            <div
              v-if="teams.length < 2"
              class="mt-4 rounded-xl border border-amber-500/20 bg-amber-500/10 p-4"
            >
              <p class="text-sm font-semibold text-amber-300">
                Teams are not available
              </p>

              <p class="mt-1 text-xs text-amber-200/70">
                Add at least two teams to your database before creating a match.
              </p>
            </div>

            <div
              v-if="form.home_team && form.home_team === form.away_team"
              class="mt-4 rounded-xl border border-red-500/20 bg-red-500/10 p-3 text-sm text-red-300"
            >
              Home and away teams must be different.
            </div>
          </div>

          <div class="h-px bg-slate-800"></div>

          <!-- Competition and Kickoff -->
          <div>
            <h3 class="mb-4 text-sm font-semibold text-slate-200">
              Match Information
            </h3>

            <div class="space-y-4">

              <div>
                <label for="competition" class="mb-2 block text-xs font-medium text-slate-400">
                  Competition
                </label>

                <select
                  id="competition"
                  v-model="form.competition"
                  class="w-full rounded-xl border border-slate-700 bg-[#070A0F] px-4 py-3 text-sm text-white outline-none focus:border-indigo-500"
                >
                  <option value="">Friendly / No competition</option>

                  <option
                    v-for="item in competitions"
                    :key="item.id"
                    :value="String(item.id)"
                  >
                    {{ item.name }}
                  </option>
                </select>
              </div>

              <div>
                <label for="kickoff" class="mb-2 block text-xs font-medium text-slate-400">
                  Kick-off Date & Time
                </label>

                <input
                  id="kickoff"
                  v-model="form.kickoff"
                  type="datetime-local"
                  required
                  class="w-full rounded-xl border border-slate-700 bg-[#070A0F] px-4 py-3 text-sm text-white outline-none focus:border-indigo-500"
                />
              </div>
            </div>
          </div>

          <div class="h-px bg-slate-800"></div>

          <!-- Score -->
          <div>
            <h3 class="mb-4 text-sm font-semibold text-slate-200">
              Match Score
            </h3>

            <div class="grid grid-cols-2 gap-4">

              <div>
                <label for="home-score" class="mb-2 block text-xs font-medium text-slate-400">
                  Home Score
                </label>

                <input
                  id="home-score"
                  v-model="form.home_score"
                  type="number"
                  min="0"
                  step="1"
                  placeholder="—"
                  class="w-full rounded-xl border border-slate-700 bg-[#070A0F] px-4 py-3 text-sm text-white outline-none focus:border-indigo-500"
                />
              </div>

              <div>
                <label for="away-score" class="mb-2 block text-xs font-medium text-slate-400">
                  Away Score
                </label>

                <input
                  id="away-score"
                  v-model="form.away_score"
                  type="number"
                  min="0"
                  step="1"
                  placeholder="—"
                  class="w-full rounded-xl border border-slate-700 bg-[#070A0F] px-4 py-3 text-sm text-white outline-none focus:border-indigo-500"
                />
              </div>
            </div>
          </div>

          <!-- Status -->
          <div>
            <label for="match-status" class="mb-2 block text-xs font-medium text-slate-400">
              Match Status
            </label>

            <select
              id="match-status"
              v-model="form.status"
              class="w-full rounded-xl border border-slate-700 bg-[#070A0F] px-4 py-3 text-sm text-white outline-none focus:border-indigo-500"
            >
              <option value="scheduled">Scheduled</option>
              <option value="live">Live</option>
              <option value="finished">Finished</option>
              <option value="postponed">Postponed</option>
            </select>
          </div>

          <!-- Error -->
          <div
            v-if="formError"
            class="rounded-xl border border-red-500/20 bg-red-500/10 p-4 text-sm text-red-300"
          >
            {{ formError }}
          </div>

          <!-- Actions -->
          <div class="flex flex-col-reverse gap-3 border-t border-slate-800 pt-5 sm:flex-row sm:justify-end">

            <button
              type="button"
              :disabled="saving"
              class="rounded-xl border border-slate-700 px-5 py-3 text-sm font-medium text-slate-300 transition hover:bg-slate-800 disabled:opacity-50"
              @click="closeModal"
            >
              Cancel
            </button>

            <button
              type="submit"
              :disabled="
                saving ||
                teams.length < 2 ||
                !form.home_team ||
                !form.away_team ||
                form.home_team === form.away_team
              "
              class="rounded-xl bg-indigo-600 px-6 py-3 text-sm font-semibold text-white transition hover:bg-indigo-500 disabled:cursor-not-allowed disabled:opacity-50"
            >
              {{
                saving
                  ? 'Saving...'
                  : editingId === null
                    ? 'Create Match'
                    : 'Save Changes'
              }}
            </button>

          </div>
        </form>
      </section>
    </div>

    <!-- VIEW MATCH MODAL -->
    <div
      v-if="viewingMatch"
      class="fixed inset-0 z-50 flex items-center justify-center bg-black/80 p-4 backdrop-blur-sm"
      @click.self="viewingMatch = null"
    >
      <section class="w-full max-w-lg overflow-hidden rounded-2xl border border-slate-700 bg-[#0F141C] shadow-2xl">

        <div class="flex items-center justify-between border-b border-slate-800 p-6">
          <div>
            <p class="text-xs font-semibold uppercase tracking-widest text-indigo-400">
              Match Details
            </p>

            <h2 class="mt-2 text-xl font-bold">
              {{ viewingMatch.competition_name || 'Friendly Match' }}
            </h2>
          </div>

          <button
            type="button"
            aria-label="Close details"
            class="text-2xl text-slate-400 hover:text-white"
            @click="viewingMatch = null"
          >
            ×
          </button>
        </div>

        <!-- Match Scoreboard -->
        <div class="p-7">

          <div class="grid grid-cols-[1fr_auto_1fr] items-center gap-4 text-center">

            <div>
              <div class="mx-auto flex h-16 w-16 items-center justify-center rounded-2xl bg-slate-800 text-lg font-bold text-indigo-300">
                {{ initials(viewingMatch.home_team_name) }}
              </div>

              <p class="mt-3 text-sm font-semibold">
                {{ viewingMatch.home_team_name }}
              </p>

              <p class="mt-1 text-xs text-slate-500">
                Home
              </p>
            </div>

            <div>
              <p class="text-3xl font-bold tracking-wider">
                {{ displayScore(viewingMatch.home_score) }}
                <span class="text-slate-600">:</span>
                {{ displayScore(viewingMatch.away_score) }}
              </p>

              <span
                class="mt-3 inline-flex rounded-full px-3 py-1 text-[10px] font-semibold"
                :class="statusClasses(viewingMatch.status)"
              >
                {{ statusLabel(viewingMatch.status) }}
              </span>
            </div>

            <div>
              <div class="mx-auto flex h-16 w-16 items-center justify-center rounded-2xl bg-slate-800 text-lg font-bold text-emerald-300">
                {{ initials(viewingMatch.away_team_name) }}
              </div>

              <p class="mt-3 text-sm font-semibold">
                {{ viewingMatch.away_team_name }}
              </p>

              <p class="mt-1 text-xs text-slate-500">
                Away
              </p>
            </div>

          </div>

          <!-- Match Metadata -->
          <div class="mt-8 space-y-4 rounded-xl border border-slate-800 bg-[#070A0F] p-5">

            <div class="flex justify-between gap-4">
              <span class="text-sm text-slate-500">Competition</span>
              <span class="text-right text-sm text-slate-200">
                {{ viewingMatch.competition_name || 'Friendly Match' }}
              </span>
            </div>

            <div class="flex justify-between gap-4">
              <span class="text-sm text-slate-500">Date</span>
              <span class="text-sm text-slate-200">
                {{ formatDate(viewingMatch.kickoff) }}
              </span>
            </div>

            <div class="flex justify-between gap-4">
              <span class="text-sm text-slate-500">Kick-off</span>
              <span class="text-sm text-slate-200">
                {{ formatTime(viewingMatch.kickoff) }}
              </span>
            </div>

            <div class="flex justify-between gap-4">
              <span class="text-sm text-slate-500">Season</span>
              <span class="text-sm text-slate-200">
                {{ competitionSeason(viewingMatch.competition) }}
              </span>
            </div>

            <div class="flex justify-between gap-4">
              <span class="text-sm text-slate-500">Match ID</span>
              <span class="text-sm text-slate-200">
                #{{ viewingMatch.id }}
              </span>
            </div>

          </div>

          <button
            type="button"
            class="mt-6 w-full rounded-xl bg-slate-800 px-4 py-3 text-sm font-semibold text-slate-200 transition hover:bg-slate-700"
            @click="viewingMatch = null"
          >
            Close Details
          </button>
        </div>
      </section>
    </div>

    <!-- Footer -->
    <footer class="flex flex-col justify-between gap-2 border-t border-slate-800/70 pt-5 text-xs text-slate-600 sm:flex-row">
      <p>FIDS Administration Panel</p>
      <p>Football Intelligence Decision System · Match Management</p>
    </footer>

  </div>
</template>








<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'

type MatchStatus = 'scheduled' | 'live' | 'finished' | 'postponed'
type SelectValue = number | string | { id?: number; name?: string } | null

interface Team {
  id: number
  name: string
}

interface Competition {
  id: number
  name: string
  season?: string
}

interface Match {
  id: number
  home_team: number
  away_team: number
  competition: number | null
  kickoff: string
  home_score: number | null
  away_score: number | null
  status: MatchStatus
  home_team_name: string
  away_team_name: string
  competition_name: string | null
}

interface MatchForm {
  home_team: number
  away_team: number
  competition: string
  kickoff: string
  home_score: string
  away_score: string
  status: MatchStatus
}

const API_BASE = (
  import.meta.env.VITE_API_BASE_URL ||
  'http://127.0.0.1:8000/api/v1'
).replace(/\/$/, '')

// State
const matches = ref<Match[]>([])
const teams = ref<Team[]>([])
const competitions = ref<Competition[]>([])

const loading = ref(false)
const saving = ref(false)
const deletingId = ref<number | null>(null)

const pageError = ref('')
const formError = ref('')
const notice = ref('')

const searchQuery = ref('')
const selectedStatus = ref('All')
const selectedCompetition = ref('All')
const selectedDate = ref('')

const showModal = ref(false)
const editingId = ref<number | null>(null)
const viewingMatch = ref<Match | null>(null)

let loadRequestId = 0

const emptyForm = (): MatchForm => ({
  home_team: 0,
  away_team: 0,
  competition: '',
  kickoff: '',
  home_score: '',
  away_score: '',
  status: 'scheduled',
})

const form = ref<MatchForm>(emptyForm())

// Authentication
function getToken(): string {
  return (
    localStorage.getItem('fids_access_token') ||
    localStorage.getItem('token') ||
    ''
  )
}

// Error handling
function extractErrorMessage(data: unknown): string {
  if (!data) return ''

  if (typeof data === 'string') return data

  if (typeof data !== 'object') return String(data)

  const errorData = data as Record<string, unknown>

  if (typeof errorData.detail === 'string') return errorData.detail
  if (typeof errorData.message === 'string') return errorData.message

  if (Array.isArray(errorData.non_field_errors)) {
    return errorData.non_field_errors.join(', ')
  }

  return Object.entries(errorData)
    .map(([key, value]) => {
      const message = Array.isArray(value)
        ? value.join(', ')
        : typeof value === 'object'
          ? extractErrorMessage(value)
          : String(value)

      return message ? `${key}: ${message}` : ''
    })
    .filter(Boolean)
    .join(' | ')
}

// API helper
async function api<T>(
  path: string,
  options: RequestInit = {},
): Promise<T> {
  const headers = new Headers(options.headers)
  const token = getToken()

  headers.set('Accept', 'application/json')

  if (options.body) {
    headers.set('Content-Type', 'application/json')
  }

  if (token) {
    headers.set('Authorization', `Bearer ${token}`)
  }

  let response: Response

  try {
    response = await fetch(`${API_BASE}${path}`, {
      ...options,
      headers,
    })
  } catch {
    throw new Error(
      'Cannot connect to Django. Make sure the backend is running on port 8000.',
    )
  }

  if (response.status === 204) {
    return undefined as T
  }

  const responseText = await response.text()
  let data: unknown = null

  if (responseText) {
    try {
      data = JSON.parse(responseText)
    } catch {
      data = responseText
    }
  }

  if (!response.ok) {
    if (response.status === 401) {
      throw new Error('Your session has expired. Please log in again.')
    }

    if (response.status === 403) {
      throw new Error('You do not have permission to perform this action.')
    }

    if (response.status === 404) {
      throw new Error(`API endpoint not found: ${path}`)
    }

    throw new Error(
      extractErrorMessage(data) || `Request failed (${response.status}).`,
    )
  }

  return data as T
}

// Response normalization
function unwrapList<T>(response: unknown): T[] {
  if (Array.isArray(response)) return response as T[]

  if (!response || typeof response !== 'object') return []

  const data = response as Record<string, unknown>

  const possibleLists = [
    data.results,
    data.data,
    data.items,
    data.matches,
    data.teams,
    data.competitions,
  ]

  for (const list of possibleLists) {
    if (Array.isArray(list)) return list as T[]
  }

  return []
}

function relationId(value: SelectValue): number {
  if (typeof value === 'number') return value
  if (typeof value === 'string') return Number(value) || 0
  if (value && typeof value === 'object') return Number(value.id) || 0
  return 0
}

function relationName(value: SelectValue): string {
  if (value && typeof value === 'object') return value.name || ''
  return ''
}

function normalizeTeam(value: unknown): Team {
  const team = (value || {}) as Record<string, unknown>

  return {
    id: Number(team.id) || 0,
    name: String(team.name || team.short_name || 'Unknown team'),
  }
}

function normalizeCompetition(value: unknown): Competition {
  const competition = (value || {}) as Record<string, unknown>

  return {
    id: Number(competition.id) || 0,
    name: String(competition.name || 'Unknown competition'),
    season: competition.season ? String(competition.season) : '',
  }
}

function normalizeMatch(value: unknown): Match {
  const item = (value || {}) as Record<string, unknown>

  const homeRelation = item.home_team as SelectValue
  const awayRelation = item.away_team as SelectValue
  const competitionRelation = item.competition as SelectValue

  const homeTeamId = relationId(homeRelation)
  const awayTeamId = relationId(awayRelation)
  const competitionId = relationId(competitionRelation)

  const allowedStatuses: MatchStatus[] = [
    'scheduled',
    'live',
    'finished',
    'postponed',
  ]

  const rawStatus = String(item.status || 'scheduled')
  const status = allowedStatuses.includes(rawStatus as MatchStatus)
    ? (rawStatus as MatchStatus)
    : 'scheduled'

  return {
    id: Number(item.id) || 0,
    home_team: homeTeamId,
    away_team: awayTeamId,
    competition: competitionId || null,
    kickoff: String(item.kickoff || item.date || ''),
    home_score:
      item.home_score === null || item.home_score === undefined
        ? null
        : Number(item.home_score),
    away_score:
      item.away_score === null || item.away_score === undefined
        ? null
        : Number(item.away_score),
    status,
    home_team_name: String(
      item.home_team_name ||
      relationName(homeRelation) ||
      'Unknown team',
    ),
    away_team_name: String(
      item.away_team_name ||
      relationName(awayRelation) ||
      'Unknown team',
    ),
    competition_name:
      item.competition_name
        ? String(item.competition_name)
        : relationName(competitionRelation) || null,
  }
}

// Load all page data
async function loadData() {
  const requestId = ++loadRequestId

  loading.value = true
  pageError.value = ''

  try {
    const [matchResponse, teamResponse, competitionResponse] =
      await Promise.all([
        api<unknown>('/matches/'),
        api<unknown>('/teams/'),
        api<unknown>('/competitions/'),
      ])

    // Ignore an older request if a newer refresh has started.
    if (requestId !== loadRequestId) return

    matches.value = unwrapList<unknown>(matchResponse)
      .map(normalizeMatch)
      .filter((match) => match.id > 0)

    teams.value = unwrapList<unknown>(teamResponse)
      .map(normalizeTeam)
      .filter((team) => team.id > 0)

    competitions.value = unwrapList<unknown>(competitionResponse)
      .map(normalizeCompetition)
      .filter((competition) => competition.id > 0)

    console.log('FIDS admin data:', {
      matches: matches.value.length,
      teams: teams.value.length,
      competitions: competitions.value.length,
    })

    if (teams.value.length === 0) {
      pageError.value =
        'No teams were returned by the API. Add teams to the Django database before creating matches.'
    }
  } catch (error) {
    if (requestId !== loadRequestId) return

    pageError.value =
      error instanceof Error
        ? error.message
        : 'Unable to load data from the server.'
  } finally {
    if (requestId === loadRequestId) {
      loading.value = false
    }
  }
}

// Search and filters
const filteredMatches = computed(() => {
  const query = searchQuery.value.trim().toLowerCase()

  return matches.value
    .filter((match) => {
      const searchableValues = [
        match.home_team_name,
        match.away_team_name,
        match.competition_name || '',
      ]

      const matchesSearch =
        !query ||
        searchableValues.some((value) =>
          value.toLowerCase().includes(query),
        )

      const matchesStatus =
        selectedStatus.value === 'All' ||
        match.status === selectedStatus.value

      const matchesCompetition =
        selectedCompetition.value === 'All' ||
        String(match.competition ?? '') === selectedCompetition.value

      const matchesDate =
        !selectedDate.value ||
        match.kickoff.slice(0, 10) === selectedDate.value

      return (
        matchesSearch &&
        matchesStatus &&
        matchesCompetition &&
        matchesDate
      )
    })
    .sort((a, b) => a.kickoff.localeCompare(b.kickoff))
})

// Status tabs
const statusTabs = computed(() => [
  {
    value: 'All',
    label: 'All Matches',
    count: matches.value.length,
  },
  ...(
    ['live', 'scheduled', 'finished', 'postponed'] as MatchStatus[]
  ).map((status) => ({
    value: status,
    label: statusLabel(status),
    count: matches.value.filter((match) => match.status === status).length,
  })),
])

// Statistics
const statCards = computed(() => [
  {
    label: 'Total Matches',
    value: matches.value.length,
    description: 'Matches in the database',
    icon: '⚽',
    iconClass: 'bg-indigo-500/10 text-indigo-400',
  },
  {
    label: 'Live Matches',
    value: matches.value.filter((m) => m.status === 'live').length,
    description: 'Currently marked live',
    icon: '●',
    iconClass: 'bg-red-500/10 text-red-400',
  },
  {
    label: 'Scheduled',
    value: matches.value.filter((m) => m.status === 'scheduled').length,
    description: 'Fixtures awaiting kick-off',
    icon: '◷',
    iconClass: 'bg-blue-500/10 text-blue-400',
  },
  {
    label: 'Finished',
    value: matches.value.filter((m) => m.status === 'finished').length,
    description: 'Matches completed',
    icon: '✓',
    iconClass: 'bg-emerald-500/10 text-emerald-400',
  },
])

// Status helpers
function statusLabel(status: string): string {
  const labels: Record<string, string> = {
    scheduled: 'Scheduled',
    live: 'Live',
    finished: 'Finished',
    postponed: 'Postponed',
  }

  return labels[status] || status
}

function statusClasses(status: MatchStatus): string {
  const classes: Record<MatchStatus, string> = {
    live: 'bg-red-500/10 text-red-400',
    finished: 'bg-emerald-500/10 text-emerald-400',
    scheduled: 'bg-blue-500/10 text-blue-400',
    postponed: 'bg-amber-500/10 text-amber-400',
  }

  return classes[status]
}

function statusDotClasses(status: MatchStatus): string {
  const classes: Record<MatchStatus, string> = {
    live: 'bg-red-400 animate-pulse',
    finished: 'bg-emerald-400',
    scheduled: 'bg-blue-400',
    postponed: 'bg-amber-400',
  }

  return classes[status]
}

// Display helpers
function displayScore(score: number | null): number | string {
  return score === null ? '—' : score
}

function initials(name = ''): string {
  return name.trim().slice(0, 3).toUpperCase() || '—'
}

function formatDate(value: string): string {
  if (!value) return '—'

  const date = new Date(value)
  if (Number.isNaN(date.getTime())) return '—'

  return date.toLocaleDateString('en-GB', {
    year: 'numeric',
    month: 'short',
    day: '2-digit',
  })
}

function formatTime(value: string): string {
  if (!value) return '—'

  const date = new Date(value)
  if (Number.isNaN(date.getTime())) return '—'

  return date.toLocaleTimeString('en-GB', {
    hour: '2-digit',
    minute: '2-digit',
  })
}

function competitionSeason(id: number | null): string {
  if (id === null) return '—'

  return (
    competitions.value.find((competition) => competition.id === id)
      ?.season || '—'
  )
}

// Reset filters
function resetFilters() {
  searchQuery.value = ''
  selectedStatus.value = 'All'
  selectedCompetition.value = 'All'
  selectedDate.value = ''
}

// Create modal
function openCreateModal() {
  editingId.value = null
  form.value = emptyForm()
  formError.value = ''
  showModal.value = true
}

// Edit modal
function openEditModal(match: Match) {
  editingId.value = match.id

  form.value = {
    home_team: match.home_team,
    away_team: match.away_team,
    competition: match.competition ? String(match.competition) : '',
    kickoff: toLocalDateTime(match.kickoff),
    home_score:
      match.home_score === null ? '' : String(match.home_score),
    away_score:
      match.away_score === null ? '' : String(match.away_score),
    status: match.status,
  }

  formError.value = ''
  showModal.value = true
}

// Date helpers
function toLocalDateTime(value: string): string {
  if (!value) return ''

  const date = new Date(value)
  if (Number.isNaN(date.getTime())) return ''

  const localDate = new Date(
    date.getTime() - date.getTimezoneOffset() * 60000,
  )

  return localDate.toISOString().slice(0, 16)
}

function closeModal() {
  if (saving.value) return

  showModal.value = false
  editingId.value = null
  formError.value = ''
}

// Form validation
function validateForm(): string {
  if (teams.value.length < 2) {
    return 'At least two teams must exist before creating a match.'
  }

  if (!form.value.home_team || !form.value.away_team) {
    return 'Please select both teams.'
  }

  if (form.value.home_team === form.value.away_team) {
    return 'Home and away teams must be different.'
  }

  if (!teams.value.some((team) => team.id === form.value.home_team)) {
    return 'The selected home team is not available. Refresh the page.'
  }

  if (!teams.value.some((team) => team.id === form.value.away_team)) {
    return 'The selected away team is not available. Refresh the page.'
  }

  if (!form.value.kickoff) {
    return 'Please select the kick-off date and time.'
  }

  if (Number.isNaN(new Date(form.value.kickoff).getTime())) {
    return 'Please enter a valid kick-off date and time.'
  }

  const scoreValues = [form.value.home_score, form.value.away_score]

  const invalidScore = scoreValues.some(
    (score) =>
      score !== '' &&
      (!Number.isInteger(Number(score)) || Number(score) < 0),
  )

  if (invalidScore) {
    return 'Scores must be non-negative whole numbers.'
  }

  if (
    form.value.status === 'finished' &&
    scoreValues.some((score) => score === '')
  ) {
    return 'Enter both scores for a finished match.'
  }

  if (
    (form.value.home_score === '') !==
    (form.value.away_score === '')
  ) {
    return 'Enter both scores or leave both scores empty.'
  }

  return ''
}

// Create / update
async function saveMatch() {
  if (saving.value) return

  formError.value = ''
  notice.value = ''

  const validationError = validateForm()

  if (validationError) {
    formError.value = validationError
    return
  }

  const payload = {
    home_team: Number(form.value.home_team),
    away_team: Number(form.value.away_team),
    competition: form.value.competition
      ? Number(form.value.competition)
      : null,
    kickoff: new Date(form.value.kickoff).toISOString(),
    home_score:
      form.value.home_score === ''
        ? null
        : Number(form.value.home_score),
    away_score:
      form.value.away_score === ''
        ? null
        : Number(form.value.away_score),
    status: form.value.status,
  }

  saving.value = true
  const isEditing = editingId.value !== null

  try {
    const endpoint = isEditing
      ? `/matches/${editingId.value}/`
      : '/matches/'

    await api(endpoint, {
      method: isEditing ? 'PATCH' : 'POST',
      body: JSON.stringify(payload),
    })

    showModal.value = false
    editingId.value = null
    form.value = emptyForm()

    notice.value = isEditing
      ? 'Match updated successfully.'
      : 'Match created successfully.'

    await loadData()
  } catch (error) {
    formError.value =
      error instanceof Error ? error.message : 'Unable to save match.'
  } finally {
    saving.value = false
  }
}

// View details
function viewMatch(match: Match) {
  viewingMatch.value = match
}

// Delete
async function deleteMatch(match: Match) {
  if (deletingId.value !== null) return

  const confirmed = window.confirm(
    `Delete ${match.home_team_name} vs ${match.away_team_name}?`,
  )

  if (!confirmed) return

  deletingId.value = match.id
  pageError.value = ''
  notice.value = ''

  try {
    await api(`/matches/${match.id}/`, {
      method: 'DELETE',
    })

    notice.value = 'Match deleted successfully.'

    if (viewingMatch.value?.id === match.id) {
      viewingMatch.value = null
    }

    await loadData()
  } catch (error) {
    pageError.value =
      error instanceof Error ? error.message : 'Unable to delete match.'
  } finally {
    deletingId.value = null
  }
}

onMounted(loadData)
</script>