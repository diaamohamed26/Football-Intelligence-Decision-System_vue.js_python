<template>
  <main
    class="flex min-h-[calc(100vh-64px)] items-center justify-center bg-[#070A0F] px-6 text-[#F5F7FA]"
  >
    <div class="text-center">
      <p class="text-sm font-semibold uppercase tracking-[0.3em] text-[#B7FF3C]">
        FIDS
      </p>

      <h1 class="mt-4 text-7xl font-black tracking-tight sm:text-8xl">
        404
      </h1>

      <h2 class="mt-4 text-2xl font-bold">
        Page not found
      </h2>

      <p class="mx-auto mt-3 max-w-md text-[#8993A4]">
        The page you're looking for doesn't exist or may have been moved.
      </p>

      <RouterLink
        to="/"
        class="mt-8 inline-flex rounded-xl bg-[#B7FF3C] px-6 py-3 font-semibold text-[#070A0F] transition hover:opacity-90"
      >
        Back to FIDS
      </RouterLink>
    </div>
  </main>
</template>