<script setup lang="ts">
import { ref, nextTick } from 'vue'
import { Send, Sparkles, Bot, User, Trash2 } from 'lucide-vue-next'

interface ChatMessage {
  id: number
  role: 'user' | 'assistant'
  content: string
  createdAt: Date
}

const API_BASE =
  import.meta.env.VITE_API_BASE_URL ||
  'http://127.0.0.1:8000/api/v1'

const prompt = ref('')
const isLoading = ref(false)
const errorMessage = ref('')
const messages = ref<ChatMessage[]>([])
const chatContainer = ref<HTMLElement | null>(null)

const suggestions = [
  'Analyze today’s top matches',
  'Find young Egyptian talents',
  'Compare Salah and Saka',
  'Which teams have the strongest momentum?',
]

const scrollToBottom = async () => {
  await nextTick()

  chatContainer.value?.scrollTo({
    top: chatContainer.value.scrollHeight,
    behavior: 'smooth',
  })
}

const askAI = async () => {
  const question = prompt.value.trim()

  if (!question || isLoading.value) return

  const token =
    localStorage.getItem('fids_access_token') ||
    localStorage.getItem('token')

  if (!token) {
    errorMessage.value = 'You must log in first. Please sign in and try again.'
    return
  }

  messages.value.push({
    id: Date.now(),
    role: 'user',
    content: question,
    createdAt: new Date(),
  })

  prompt.value = ''
  errorMessage.value = ''
  isLoading.value = true

  await scrollToBottom()

  try {
    const response = await fetch(`${API_BASE}/intelligence/chat/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify({
        prompt: question,
        save: true,
      }),
    })

    const data = await response.json().catch(() => ({}))

    if (response.status === 401) {
      throw new Error(
        'Your session has expired or your access token is invalid. Please log in again.',
      )
    }

    if (!response.ok) {
      throw new Error(
        data.detail ||
        data.error ||
        `Request failed with status ${response.status}`,
      )
    }

    const answer = data.answer || data.response || data.message

    if (!answer || typeof answer !== 'string') {
      throw new Error('The AI API returned an invalid response.')
    }

    messages.value.push({
      id: Date.now() + 1,
      role: 'assistant',
      content: answer,
      createdAt: new Date(),
    })

    await scrollToBottom()
  } catch (error) {
    errorMessage.value =
      error instanceof Error
        ? error.message
        : 'Something went wrong. Please try again.'
  } finally {
    isLoading.value = false
  }
}

const useSuggestion = (suggestion: string) => {
  prompt.value = suggestion
}

const clearChat = () => {
  messages.value = []
  errorMessage.value = ''
}
</script>

<template>
  <section class="min-h-[calc(100vh-64px)] bg-[#070A0F] px-4 py-10 text-[#F5F7FA]">
    <div class="mx-auto max-w-5xl">
      <header class="mb-10 text-center">
        <div class="mx-auto mb-5 flex h-14 w-14 items-center justify-center rounded-2xl border border-[#202936] bg-[#0F141C]">
          <Sparkles class="h-7 w-7 text-[#B7FF3C]" />
        </div>

        <p class="mb-3 text-sm font-semibold uppercase tracking-[0.25em] text-[#B7FF3C]">
          FIDS Intelligence
        </p>

        <h1 class="text-4xl font-bold tracking-tight sm:text-5xl">
          Ask football. Get intelligence.
        </h1>

        <p class="mx-auto mt-5 max-w-2xl text-base leading-7 text-[#8993A4]">
          Analyze matches, discover players, compare teams and explore
          football intelligence using FIDS AI.
        </p>
      </header>

      <div class="overflow-hidden rounded-3xl border border-[#202936] bg-[#0F141C] shadow-2xl">
        <div class="flex items-center justify-between border-b border-[#202936] px-5 py-4">
          <div class="flex items-center gap-3">
            <div class="flex h-10 w-10 items-center justify-center rounded-xl bg-[#B7FF3C]/10">
              <Bot class="h-5 w-5 text-[#B7FF3C]" />
            </div>

            <div>
              <h2 class="font-semibold">FIDS AI Assistant</h2>
              <p class="text-xs text-[#8993A4]">Football Intelligence</p>
            </div>
          </div>

          <button
            v-if="messages.length"
            type="button"
            class="flex items-center gap-2 text-xs text-[#8993A4] transition hover:text-red-400"
            @click="clearChat"
          >
            <Trash2 class="h-4 w-4" />
            Clear chat
          </button>
        </div>

        <div
          ref="chatContainer"
          class="max-h-[550px] min-h-[300px] space-y-6 overflow-y-auto p-5 sm:p-7"
        >
          <div v-if="!messages.length" class="py-12 text-center">
            <Sparkles class="mx-auto mb-4 h-9 w-9 text-[#B7FF3C]" />

            <h3 class="text-lg font-semibold">
              Welcome to FIDS Intelligence
            </h3>

            <p class="mt-2 text-sm text-[#8993A4]">
              Ask your first football question to get started.
            </p>
          </div>

          <div
            v-for="message in messages"
            :key="message.id"
            class="flex gap-3"
            :class="message.role === 'user' ? 'flex-row-reverse' : ''"
          >
            <div
              class="flex h-9 w-9 shrink-0 items-center justify-center rounded-xl"
              :class="message.role === 'user' ? 'bg-[#B7FF3C]/10' : 'bg-[#202936]'"
            >
              <User
                v-if="message.role === 'user'"
                class="h-4 w-4 text-[#B7FF3C]"
              />
              <Bot v-else class="h-4 w-4 text-[#B7FF3C]" />
            </div>

            <div
              class="max-w-[85%] rounded-2xl px-4 py-3 text-sm leading-7"
              :class="message.role === 'user'
                ? 'bg-[#B7FF3C] text-[#070A0F]'
                : 'border border-[#202936] bg-[#070A0F] text-[#F5F7FA]'"
            >
              <p class="whitespace-pre-wrap">{{ message.content }}</p>
            </div>
          </div>

          <div v-if="isLoading" class="flex items-center gap-3">
            <div class="flex h-9 w-9 items-center justify-center rounded-xl bg-[#202936]">
              <Bot class="h-4 w-4 text-[#B7FF3C]" />
            </div>

            <div class="rounded-2xl border border-[#202936] bg-[#070A0F] px-5 py-3">
              <div class="flex items-center gap-2">
                <span class="h-2 w-2 animate-bounce rounded-full bg-[#B7FF3C]"></span>
                <span class="h-2 w-2 animate-bounce rounded-full bg-[#B7FF3C] [animation-delay:150ms]"></span>
                <span class="h-2 w-2 animate-bounce rounded-full bg-[#B7FF3C] [animation-delay:300ms]"></span>
                <span class="ml-2 text-xs text-[#8993A4]">Analyzing...</span>
              </div>
            </div>
          </div>
        </div>

        <div
          v-if="errorMessage"
          class="mx-5 mb-3 rounded-xl border border-red-500/20 bg-red-500/10 p-3 text-sm text-red-400"
        >
          {{ errorMessage }}
        </div>

        <div class="border-t border-[#202936] p-4 sm:p-5">
          <textarea
            v-model="prompt"
            rows="3"
            placeholder="Ask something about football..."
            class="w-full resize-none rounded-2xl border border-[#202936] bg-[#070A0F] p-4 text-sm text-[#F5F7FA] outline-none transition placeholder:text-[#8993A4] focus:border-[#B7FF3C]"
            @keydown.ctrl.enter.prevent="askAI"
            @keydown.meta.enter.prevent="askAI"
          ></textarea>

          <div class="mt-3 flex items-center justify-between gap-3">
            <span class="text-xs text-[#8993A4]">
              Press Ctrl + Enter to ask
            </span>

            <button
              type="button"
              :disabled="!prompt.trim() || isLoading"
              class="inline-flex items-center gap-2 rounded-xl bg-[#B7FF3C] px-5 py-3 text-sm font-semibold text-[#070A0F] transition hover:opacity-90 disabled:cursor-not-allowed disabled:opacity-40"
              @click="askAI"
            >
              <Send class="h-4 w-4" />
              {{ isLoading ? 'Analyzing...' : 'Ask FIDS AI' }}
            </button>
          </div>
        </div>
      </div>

      <div v-if="!messages.length" class="mt-8">
        <p class="mb-4 text-sm font-medium text-[#8993A4]">Try asking</p>

        <div class="grid gap-3 sm:grid-cols-2">
          <button
            v-for="suggestion in suggestions"
            :key="suggestion"
            type="button"
            class="rounded-2xl border border-[#202936] bg-[#0F141C] p-4 text-left text-sm text-[#F5F7FA] transition hover:border-[#B7FF3C] hover:bg-[#151C26]"
            @click="useSuggestion(suggestion)"
          >
            {{ suggestion }}
          </button>
        </div>
      </div>

      <div class="mt-12 grid gap-4 sm:grid-cols-3">
        <div class="rounded-2xl border border-[#202936] bg-[#0F141C] p-5">
          <div class="mb-3 text-[#B7FF3C]">01</div>
          <h3 class="font-semibold">Match Analyst</h3>
          <p class="mt-2 text-sm leading-6 text-[#8993A4]">
            Tactical and statistical match analysis.
          </p>
        </div>

        <div class="rounded-2xl border border-[#202936] bg-[#0F141C] p-5">
          <div class="mb-3 text-[#B7FF3C]">02</div>
          <h3 class="font-semibold">Scout Analyst</h3>
          <p class="mt-2 text-sm leading-6 text-[#8993A4]">
            Discover players based on role, age and tactical fit.
          </p>
        </div>

        <div class="rounded-2xl border border-[#202936] bg-[#0F141C] p-5">
          <div class="mb-3 text-[#B7FF3C]">03</div>
          <h3 class="font-semibold">Transfer Analyst</h3>
          <p class="mt-2 text-sm leading-6 text-[#8993A4]">
            Recruitment intelligence and player comparisons.
          </p>
        </div>
      </div>
    </div>
  </section>
</template>
